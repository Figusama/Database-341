from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database.database import get_session
from backend.conference.models import conference
from backend.user.models import app_user, author, reviewer



router = APIRouter(tags=['conference'])

@router.get("/conferences")
def list_conferences(session : Session = Depends(get_session)):
    rows = session.exec(
        select(conference).order_by(conference.acronym)
    ).all()

    return [
        {"conference_id": c.conference_id, "name": c.name, "acronym": c.acronym, "city": c.city}
        for c in rows
    ]


@router.get("/authors")
def list_authors(session : Session = Depends(get_session)):
    rows = session.exec(
        select(app_user)
        .join(author, author.author_id == app_user.user_id)
        .order_by(app_user.surname, app_user.given_name)
    ).all()
    return [
        {"author_id": u.user_id, "given_name": u.given_name, "surname": u.surname, "email": u.email}
        for u in rows
    ]


@router.get("/reviewers")
def list_reviewers(session : Session = Depends(get_session)):
    rows = session.exec(
        select(app_user, reviewer.years_experience)
        .join(reviewer, reviewer.reviewer_id == app_user.user_id)
        .order_by(app_user.surname, app_user.given_name)
    ).all()
    return [
        {"reviewer_id": u.user_id, "given_name": u.given_name, "surname": u.surname,
         "email": u.email, "years_experience": years}
        for u, years in rows
    ]