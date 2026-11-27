from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database.database import get_session
from backend.conference.models import conference



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