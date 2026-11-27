from sqlmodel import select

from backend.conference.models import conference_session
from backend.paper.models import paper, paper_author, review
from backend.track.models import track
from fastapi import HTTPException, status


def check_no_self_review(session, paper_id, reviewer_id) -> None:
    hit = session.exec(
        select(paper_author.author_id).where(
            paper_author.paper_id == paper_id, paper_author.author_id == reviewer_id)
    ).first()
    if hit is not None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail= "Self-review rejected: this reviewer is an author of the paper.")
        


def check_authors_not_reviewers(session, paper_id, author_ids) -> None:
    if not author_ids:
        return
    clash = session.exec(
        select(review.reviewer_id).where(
            review.paper_id == paper_id, review.reviewer_id.in_(list(author_ids)))
    ).all()
    if clash:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Author change rejected: a person on the new author list already reviews this paper.")



def check_session_assignment(session, status, track_id, session_id) -> None:

    if session_id is None:
        return
    if status != "accepted":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail= "Status must be accepted")
    track_conf = session.exec(select(track.conference_id).where(track.track_id == track_id)).first()
    if track_conf is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail= f"Track {track_id} does not exist.")
    session_conf = session.exec(
        select(conference_session.conference_id)
        .where(conference_session.session_id == session_id)
        .with_for_update(read=True)
    ).first()
    if session_conf is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail= f"Session {session_id} does not exist.")
    if session_conf != track_conf:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail= "Session assignment rejected: the paper's track and the session belong to different conferences.")
    


def check_session_conference_change(session, session_id, new_conference_id) -> None:

    bad = session.exec(
        select(paper.paper_id, paper.title)
        .join(track, track.track_id == paper.track_id)
        .where(paper.session_id == session_id, track.conference_id != new_conference_id)
    ).all()
    if bad:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail= "Session change rejected: papers assigned to this session belong to a different conference. ")