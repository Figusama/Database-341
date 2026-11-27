from fastapi import APIRouter, Depends
from database.database import get_session
from sqlmodel import Session, select
from backend.track.models import track
from backend.conference.models import conference
router = APIRouter(tags=['tracks'])

@router.get("/tracks")
def list_tracks(session : Session = Depends(get_session)):
    rows = session.exec(
        select(track).join(conference, conference.conference_id == track.conference_id).order_by(track.name)
    ).all()

    return [
        {"track_id": tr.track_id, "conference_id": tr.conference_id, "name": tr.name} for tr in rows
    ]
