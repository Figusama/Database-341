from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy import delete, exists, func
from sqlmodel import Session, select
from backend.conference.models import conference

from backend.paper.models import paper, paper_author, paper_keyword, paper_version
from backend.paper.schemas import (PaperCreate, PaperOut, PaperSummary, PaperUpdate, VersionIn, PaperAuthorIn)
from backend.paper.checks import check_authors_not_reviewers, check_no_self_review, check_session_assignment, check_session_conference_change
from backend.track.models import track
from backend.user.models import app_user
from database.database import get_session

router = APIRouter(prefix="/papers", tags=["papers"])

def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _get_paper(session: Session, paper_id: UUID, lock: bool = False):
    stmt = select(paper).where(paper.paper_id == paper_id)
    if lock:
        stmt = stmt.with_for_update()
    p = session.exec(stmt).first()
    if p is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Paper not found')
    return p

def paper_out(session: Session, p) -> dict:
    t = session.exec(
        select(track.name, conference.conference_id, conference.acronym)
        .join(conference, conference.conference_id == track.conference_id)
        .where(track.track_id == p.track_id)).first()
    authors = session.exec(
        select(paper_author, app_user)
        .join(app_user, app_user.user_id == paper_author.author_id)
        .where(paper_author.paper_id == p.paper_id)
        .order_by(paper_author.author_position)).all()
    keywords = session.exec(
        select(paper_keyword.keyword).where(paper_keyword.paper_id == p.paper_id).order_by(paper_keyword.keyword)).all()
    versions = session.exec(
        select(paper_version).where(paper_version.paper_id == p.paper_id).order_by(paper_version.version_no)).all()
    return {
        "paper_id": p.paper_id, "title": p.title, "abstract": p.abstract,
        "submission_date": p.submission_date, "status": p.status,
        "track_id": p.track_id, "track_name": t[0], "conference_id": t[1], "conference_acronym": t[2],
        "session_id": p.session_id,
        "authors": [
            {"author_id": u.user_id, "given_name": u.given_name, "surname": u.surname, "email": u.email,
             "author_position": pa.author_position, "is_corresponding": pa.is_corresponding}
            for pa, u in authors],
        "keywords": list(keywords),
        "versions": [
            {"version_no": v.version_no, "file_location": v.file_location,
             "uploaded_at": v.uploaded_at, "change_note": v.change_note} for v in versions],
    }


def _replace_authors(session: Session, paper_id: UUID, authors: list[PaperAuthorIn]) -> None:
    session.exec(delete(paper_author).where(paper_author.paper_id == paper_id))
    session.flush()
    for a in authors:
        session.add(paper_author(paper_id=paper_id, author_id=a.author_id,
                                 author_position=a.author_position, is_corresponding=a.is_corresponding))
    session.flush()


def _replace_keywords(session: Session, paper_id: UUID, keywords: list[str]) -> None:
    session.exec(delete(paper_keyword).where(paper_keyword.paper_id == paper_id))
    session.flush()
    for k in keywords:
        session.add(paper_keyword(paper_id=paper_id, keyword=k))
    session.flush()


def _add_version(session: Session, paper_id: UUID, v: VersionIn) -> None:
    last = session.exec(select(func.max(paper_version.version_no)).where(paper_version.paper_id == paper_id)).one()
    session.add(paper_version(paper_id=paper_id, version_no=(last or 0) + 1, file_location=v.file_location,
                              uploaded_at=_now(), change_note=v.change_note))
    session.flush()


@router.post("", response_model=PaperOut, status_code=201, summary="Create a paper")
def create_paper(body: PaperCreate, session: Session = Depends(get_session)):
    check_session_assignment(session, body.status, body.track_id, body.session_id)
    pid = uuid4()
    session.add(paper(paper_id=pid, track_id=body.track_id, title=body.title, abstract=body.abstract,
                      submission_date=body.submission_date or date.today(), status=body.status,
                      session_id=body.session_id))
    session.flush()
    _replace_authors(session, pid, body.authors)
    _replace_keywords(session, pid, body.keywords)
    for v in body.versions:
        _add_version(session, pid, v)
    session.commit()
    return paper_out(session, _get_paper(session, pid))


@router.get("", response_model=list[PaperSummary], summary="List papers")
def list_papers(
    status: str | None = None,
    track_id: UUID | None = None,
    conference_id: UUID | None = None,
    session_id: UUID | None = None,
    author_id: UUID | None = None,
    keyword: str | None = None,
    q: str | None = Query(None, description="substring of title or abstract"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    stmt = (
        select(paper, track.name, conference.conference_id, conference.acronym)
        .join(track, track.track_id == paper.track_id)
        .join(conference, conference.conference_id == track.conference_id)
    )
    if status:
        stmt = stmt.where(paper.status == status)
    if track_id:
        stmt = stmt.where(paper.track_id == track_id)
    if conference_id:
        stmt = stmt.where(conference.conference_id == conference_id)
    if session_id:
        stmt = stmt.where(paper.session_id == session_id)
    if author_id:
        stmt = stmt.where(exists().where(paper_author.paper_id == paper.paper_id, paper_author.author_id == author_id))
    if keyword:
        stmt = stmt.where(exists().where(paper_keyword.paper_id == paper.paper_id,
                                         func.lower(paper_keyword.keyword) == keyword.strip().lower()))
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(paper.title.ilike(like) | paper.abstract.ilike(like))
    rows = session.exec(stmt.order_by(paper.submission_date, paper.title).offset(offset).limit(limit)).all()
    return [
        {"paper_id": p.paper_id, "title": p.title, "status": p.status, "submission_date": p.submission_date,
         "track_id": p.track_id, "track_name": tn, "conference_id": cid, "conference_acronym": acr,
         "session_id": p.session_id}
        for p, tn, cid, acr in rows
    ]


@router.get("/{paper_id}", response_model=PaperOut, summary="Read one paper")
def read_paper(paper_id: UUID, session: Session = Depends(get_session)):
    return paper_out(session, _get_paper(session, paper_id))

@router.patch("/{paper_id}", response_model=PaperOut,
              summary="Update a paper")
def update_paper(paper_id: UUID, body: PaperUpdate, session: Session = Depends(get_session)):
    p = _get_paper(session, paper_id, lock=True)
    fields = body.model_fields_set

    new_status = body.status if "status" in fields else p.status
    new_track = body.track_id if "track_id" in fields else p.track_id
    new_session = body.session_id if "session_id" in fields else p.session_id
    check_session_assignment(session, new_status, new_track, new_session)

    if "authors" in fields:
        check_authors_not_reviewers(session, paper_id, [a.author_id for a in body.authors])

    for f in ("track_id", "title", "abstract", "submission_date", "status", "session_id"):
        if f in fields:
            setattr(p, f, getattr(body, f))
    session.flush()
    if "authors" in fields:
        _replace_authors(session, paper_id, body.authors)
    if "keywords" in fields:
        _replace_keywords(session, paper_id, body.keywords)
    session.commit()
    session.expire_all()
    return paper_out(session, _get_paper(session, paper_id))


@router.post("/{paper_id}/versions", response_model=PaperOut, status_code=201, summary="Upload a new version")
def add_version(paper_id: UUID, body: VersionIn, session: Session = Depends(get_session)):
    _get_paper(session, paper_id, lock=True)
    _add_version(session, paper_id, body)
    session.commit()
    return paper_out(session, _get_paper(session, paper_id))


@router.delete("/{paper_id}/versions/{version_no}", response_model=PaperOut, summary="Delete one version")
def delete_version(paper_id: UUID, version_no: int, session: Session = Depends(get_session)):
    _get_paper(session, paper_id, lock=True)
    v = session.get(paper_version, (paper_id, version_no))
    if v is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{version_no} of paper {paper_id}")
    session.delete(v)
    session.commit()
    return paper_out(session, _get_paper(session, paper_id))


@router.delete("/{paper_id}", summary="Delete a paper")
def delete_paper(paper_id: UUID, session: Session = Depends(get_session)):
    p = _get_paper(session, paper_id, lock=True)
    session.delete(p)
    session.commit()
    return {"deleted": str(paper_id)}