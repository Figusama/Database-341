from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from backend.user.models import app_user, author, author_research_area, reviewer, reviewer_expertise
from backend.user.schemas import UserCreate, UserListItem, UserOut, UserUpdate, AuthorIn, ReviewerIn
from database.database import get_session

router = APIRouter(prefix="/users", tags=["users"])


def _get_user(session: Session, user_id: UUID, lock: bool = False):
    stmt = select(app_user).where(app_user.user_id == user_id)
    if lock:
        stmt = stmt.with_for_update()
    u = session.exec(stmt).first()
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return u


def user_out(session: Session, u) -> dict:
    a = session.get(author, u.user_id)
    r = session.get(reviewer, u.user_id)
    author_data = None
    if a is not None:
        areas = session.exec(
            select(author_research_area.area_label)
            .where(author_research_area.author_id == u.user_id)
            .order_by(author_research_area.area_label)).all()
        author_data = {"orcid": a.orcid, "research_areas": list(areas)}
    reviewer_data = None
    if r is not None:
        expertise = session.exec(
            select(reviewer_expertise.area_label)
            .where(reviewer_expertise.reviewer_id == u.user_id)
            .order_by(reviewer_expertise.area_label)).all()
        reviewer_data = {"years_experience": r.years_experience, "expertise": list(expertise)}
    return {
        "user_id": u.user_id, "given_name": u.given_name, "surname": u.surname, "email": u.email,
        "affiliation": u.affiliation, "country": u.country, "phone_number": u.phone_number,
        "author": author_data, "reviewer": reviewer_data,
    }


def _set_author(session: Session, user_id: UUID, data: AuthorIn) -> None:
    a = session.get(author, user_id)
    if a is None:
        session.add(author(author_id=user_id, orcid=data.orcid))
    else:
        a.orcid = data.orcid
    session.flush()
    session.exec(delete(author_research_area).where(author_research_area.author_id == user_id))
    for label in data.research_areas:
        session.add(author_research_area(author_id=user_id, area_label=label))
    session.flush()


def _set_reviewer(session: Session, user_id: UUID, data: ReviewerIn) -> None:
    r = session.get(reviewer, user_id)
    if r is None:
        session.add(reviewer(reviewer_id=user_id, years_experience=data.years_experience))
    else:
        r.years_experience = data.years_experience
    session.flush()
    session.exec(delete(reviewer_expertise).where(reviewer_expertise.reviewer_id == user_id))
    for label in data.expertise:
        session.add(reviewer_expertise(reviewer_id=user_id, area_label=label))
    session.flush()


def _commit(session: Session, conflict_detail: str) -> None:
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        table = getattr(getattr(exc.orig, "diag", None), "table_name", None)
        detail = conflict_detail if table is None else f"{conflict_detail} (referenced by '{table}')"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.get("", response_model=list[UserListItem], summary="List users")
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(app_user).order_by(app_user.surname, app_user.given_name)).all()
    author_ids = set(session.exec(select(author.author_id)).all())
    reviewer_ids = set(session.exec(select(reviewer.reviewer_id)).all())
    return [
        {"user_id": u.user_id, "given_name": u.given_name, "surname": u.surname, "email": u.email,
         "is_author": u.user_id in author_ids, "is_reviewer": u.user_id in reviewer_ids}
        for u in users
    ]

@router.get("/{user_id}", response_model=UserOut, summary="Read one user with roles")
def read_user(user_id: UUID, session: Session = Depends(get_session)):
    return user_out(session, _get_user(session, user_id))


@router.post("", response_model=UserOut, status_code=201, summary="Create a user")
def create_user(body: UserCreate, session: Session = Depends(get_session)):
    uid = uuid4()
    session.add(app_user(
        user_id=uid, given_name=body.given_name, surname=body.surname, email=body.email,
        affiliation=body.affiliation, country=body.country, phone_number=body.phone_number))
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user with this email already exists.")
    if body.author is not None:
        _set_author(session, uid, body.author)
    if body.reviewer is not None:
        _set_reviewer(session, uid, body.reviewer)
    _commit(session, "Could not create the user")
    return user_out(session, _get_user(session, uid))


@router.patch("/{user_id}", response_model=UserOut, summary="Update a user and their roles")
def update_user(user_id: UUID, body: UserUpdate, session: Session = Depends(get_session)):
    u = _get_user(session, user_id, lock=True)
    fields = body.model_fields_set

    for f in ("given_name", "surname", "email", "affiliation", "country", "phone_number"):
        if f in fields:
            setattr(u, f, getattr(body, f))
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user with this email already exists.")

    will_be_author = body.author is not None if "author" in fields else session.get(author, user_id) is not None
    will_be_reviewer = body.reviewer is not None if "reviewer" in fields else session.get(reviewer, user_id) is not None
    if not will_be_author and not will_be_reviewer:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail="A user must be an author, a reviewer, or both.")

    try:
        if "author" in fields:
            if body.author is None:
                session.exec(delete(author).where(author.author_id == user_id))
                session.flush()
            else:
                _set_author(session, user_id, body.author)
        if "reviewer" in fields:
            if body.reviewer is None:
                session.exec(delete(reviewer).where(reviewer.reviewer_id == user_id))
                session.flush()
            else:
                _set_reviewer(session, user_id, body.reviewer)
    except IntegrityError as exc:
        session.rollback()
        table = getattr(getattr(exc.orig, "diag", None), "table_name", "another table")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Cannot remove this role: it is still referenced by '{table}'.")

    _commit(session, "Could not update the user")
    session.expire_all()
    return user_out(session, _get_user(session, user_id))


@router.delete("/{user_id}", summary="Delete a user")
def delete_user(user_id: UUID, session: Session = Depends(get_session)):
    u = _get_user(session, user_id, lock=True)
    session.delete(u)
    _commit(session, "Cannot delete this user: they still have papers, reviews, or conference duties")
    return {"deleted": str(user_id)}