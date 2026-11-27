from datetime import date
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlmodel import Session, select

from backend.paper.checks import check_no_self_review
from backend.paper.models import paper, review
from backend.paper.schemas import ReviewCreate, ReviewListItem, ReviewOut
from backend.user.models import app_user
from database.database import get_session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/reviews", tags=["reviews"])


def _get_review(session: Session, review_id: UUID, lock: bool = False):
    stmt = select(review).where(review.review_id == review_id)
    if lock:
        stmt = stmt.with_for_update()
    r = session.exec(stmt).first()
    if r is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return r


def _lock_paper(session: Session, paper_id: UUID) -> None:
    found = session.exec(select(paper.paper_id).where(paper.paper_id == paper_id).with_for_update()).first()
    if found is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail= f"Paper {paper_id} does not exist.")


def review_out(r) -> dict:
    return {
        "review_id": r.review_id, "paper_id": r.paper_id, "reviewer_id": r.reviewer_id,
        "overall_score": r.overall_score, "recommendation": r.recommendation,
        "comments_for_authors": r.comments_for_authors, "confidential_comments": r.confidential_comments,
        "review_submission_date": r.review_submission_date,
    }


@router.get("", response_model=list[ReviewListItem], summary="List reviews")
def list_reviews(
    paper_id: UUID | None = None,
    reviewer_id: UUID | None = None,
    limit: int = Query(500, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    stmt = (
        select(review, paper.title, app_user.given_name, app_user.surname)
        .join(paper, paper.paper_id == review.paper_id)
        .join(app_user, app_user.user_id == review.reviewer_id)
    )
    if paper_id:
        stmt = stmt.where(review.paper_id == paper_id)
    if reviewer_id:
        stmt = stmt.where(review.reviewer_id == reviewer_id)
    rows = session.exec(
        stmt.order_by(review.review_submission_date.desc(), review.review_id).offset(offset).limit(limit)).all()
    return [
        {"review_id": r.review_id, "paper_id": r.paper_id, "paper_title": title,
         "reviewer_id": r.reviewer_id, "reviewer_name": f"{given} {surname}",
         "overall_score": r.overall_score, "recommendation": r.recommendation,
         "review_submission_date": r.review_submission_date}
        for r, title, given, surname in rows
    ]


@router.get("/{review_id}", response_model=ReviewOut, summary="One review")
def read_review(review_id: UUID, session: Session = Depends(get_session)):
    return review_out(_get_review(session, review_id))


@router.post("", response_model=ReviewOut, status_code=201, summary="Create a review")
def create_review(body: ReviewCreate, session: Session = Depends(get_session)):
    _lock_paper(session, body.paper_id)
    check_no_self_review(session, body.paper_id, body.reviewer_id)
    rid = uuid4()
    session.add(review(
        review_id=rid, paper_id=body.paper_id, reviewer_id=body.reviewer_id, overall_score=body.overall_score,
        recommendation=body.recommendation, comments_for_authors=body.comments_for_authors,
        confidential_comments=body.confidential_comments,
        review_submission_date=body.review_submission_date or date.today()))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This review has already been reviewed")
    return review_out(_get_review(session, rid))


@router.put("/{review_id}", response_model=ReviewOut, summary="Replace a review")
def replace_review(review_id: UUID, body: ReviewCreate, session: Session = Depends(get_session)):
    r = _get_review(session, review_id, lock=True)
    _lock_paper(session, body.paper_id)
    check_no_self_review(session, body.paper_id, body.reviewer_id) 
    r.paper_id = body.paper_id
    r.reviewer_id = body.reviewer_id
    r.overall_score = body.overall_score
    r.recommendation = body.recommendation
    r.comments_for_authors = body.comments_for_authors
    r.confidential_comments = body.confidential_comments
    if body.review_submission_date is not None:
        r.review_submission_date = body.review_submission_date
    session.commit()
    session.expire_all()
    return review_out(_get_review(session, review_id))

@router.delete("/{review_id}", summary="Delete a review")
def delete_review(review_id: UUID, session: Session = Depends(get_session)):
    r = _get_review(session, review_id, lock=True)
    session.delete(r)
    session.commit()
    return {"deleted": str(review_id)}