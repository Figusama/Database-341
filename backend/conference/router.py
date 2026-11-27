from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import update
from sqlmodel import Session, select

from backend.paper.checks import check_session_conference_change
from backend.conference.models import conference_session

from backend.paper.models import paper
from backend.paper.schemas import SessionCreate, SessionOut, SessionUpdate
from database.database import get_session

router = APIRouter(prefix="/sessions", tags=["sessions"])


def _get_session_row(session: Session, session_id: UUID, lock: bool = False):
    stmt = select(conference_session).where(conference_session.session_id == session_id)
    if lock:
        stmt = stmt.with_for_update()
    s = session.exec(stmt).first()
    if s is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return s


def session_out(db: Session, s) -> dict:
    papers = db.exec(
        select(paper.paper_id, paper.title, paper.status).where(paper.session_id == s.session_id).order_by(paper.title)).all()
    return {
        "session_id": s.session_id, "conference_id": s.conference_id, "title": s.title,
        "session_date": s.session_date, "start_time": s.start_time, "end_time": s.end_time,
        "room_label": s.room_label, "chair_id": s.chair_id,
        "papers": [{"paper_id": a, "title": b, "status": c} for a, b, c in papers],
    }


@router.post("", response_model=SessionOut, status_code=201, summary="Create a session")
def create_session(body: SessionCreate, db: Session = Depends(get_session)):
    sid = uuid4()
    db.add(conference_session(
        session_id=sid, conference_id=body.conference_id, title=body.title, session_date=body.session_date,
        start_time=body.start_time, end_time=body.end_time, room_label=body.room_label, chair_id=body.chair_id))
    db.commit()
    return session_out(db, _get_session_row(db, sid))

@router.get("", response_model=list[SessionOut], summary="List sessions")
def list_sessions(
    conference_id: UUID | None = None,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_session),
):
    stmt = select(conference_session)
    if conference_id:
        stmt = stmt.where(conference_session.conference_id == conference_id)
    rows = db.exec(stmt.order_by(conference_session.session_date, conference_session.start_time).offset(offset).limit(limit)).all()
    return [session_out(db, s) for s in rows]


@router.get("/{session_id}", response_model=SessionOut, summary="Read one session with its papers")
def read_session(session_id: UUID, db: Session = Depends(get_session)):
    return session_out(db, _get_session_row(db, session_id))


@router.patch("/{session_id}", response_model=SessionOut, summary="Update a session")
def update_session(session_id: UUID, body: SessionUpdate, db: Session = Depends(get_session)):
    s = _get_session_row(db, session_id, lock=True)
    fields = body.model_fields_set
    if "conference_id" in fields and body.conference_id != s.conference_id:
        check_session_conference_change(db, session_id, body.conference_id)
    for f in ("conference_id", "title", "session_date", "start_time", "end_time", "room_label", "chair_id"):
        if f in fields:
            setattr(s, f, getattr(body, f))
    db.commit()
    db.expire_all()
    return session_out(db, _get_session_row(db, session_id))

@router.delete("/{session_id}", summary="Delete a session")
def delete_session(session_id: UUID, unschedule: bool = False, db: Session = Depends(get_session)):
    s = _get_session_row(db, session_id, lock=True)
    assigned = db.exec(select(paper.paper_id).where(paper.session_id == session_id)).all()
    if assigned and not unschedule:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Session has {len(assigned)} assigned paper(s). Unassign them, or retry with ?unschedule=true.")
    if assigned:
        db.exec(update(paper).where(paper.session_id == session_id).values(session_id=None))
        db.flush()
    db.delete(s)
    db.commit()
    return {"deleted": str(session_id), "unscheduled_papers": len(assigned)}