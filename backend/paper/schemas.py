from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date, time, datetime
from uuid import UUID
from typing import Literal

PaperStatus = Literal["submitted", "under review", "accepted", "rejected", "withdrawn"]
def _clean_labels(values: list[str], max_len: int = 100) -> list[str]:
    seen, out = set(), []
    for v in values:
        v = v.strip()
        if not v:
            continue
        if len(v) > max_len:
            raise ValueError(f"'{v[:20]}...' is longer than {max_len} characters")
        if v.lower() not in seen:
            seen.add(v.lower())
            out.append(v)
    return out

def _no_nulls(model: BaseModel, fields: tuple[str, ...]) -> None:
    for f in fields:
        if f in model.model_fields_set and getattr(model, f) is None:
            raise ValueError(f"{f} cannot be null")

class PaperAuthorIn(BaseModel):
    author_id: UUID
    author_position: int = Field(ge=1)
    is_corresponding: bool = False


class VersionIn(BaseModel):
    file_location: str = Field(min_length=1, max_length=2000)
    change_note: str | None = None


def _validate_authors(authors: list[PaperAuthorIn]) -> list[PaperAuthorIn]:
    if not authors:
        raise ValueError("a paper needs at least one author")
    if len({a.author_id for a in authors}) != len(authors):
        raise ValueError("the same author is listed twice")
    if len({a.author_position for a in authors}) != len(authors):
        raise ValueError("author_position values must be unique within a paper")
    if sum(a.is_corresponding for a in authors) != 1:
        raise ValueError("exactly one author must be marked is_corresponding")
    return authors

class PaperCreate(BaseModel):
    track_id: UUID
    title: str = Field(min_length=1)
    abstract: str = Field(min_length=1)
    submission_date: date | None = None
    status: PaperStatus = "submitted"
    session_id: UUID | None = None
    authors: list[PaperAuthorIn]
    keywords: list[str] = []
    versions: list[VersionIn] = []

    @field_validator("authors")
    @classmethod
    def _authors(cls, v):
        return _validate_authors(v)

    @field_validator("keywords")
    @classmethod
    def _kw(cls, v):
        return _clean_labels(v)


class PaperUpdate(BaseModel):
    track_id: UUID | None = None
    title: str | None = Field(None, min_length=1)
    abstract: str | None = Field(None, min_length=1)
    submission_date: date | None = None
    status: PaperStatus | None = None
    session_id: UUID | None = None
    authors: list[PaperAuthorIn] | None = None
    keywords: list[str] | None = None

    @field_validator("authors")
    @classmethod
    def _authors(cls, v):
        return v if v is None else _validate_authors(v)

    @field_validator("keywords")
    @classmethod
    def _kw(cls, v):
        return v if v is None else _clean_labels(v)

    @model_validator(mode="after")
    def _nulls(self):
        _no_nulls(self, ("track_id", "title", "abstract", "submission_date", "status", "authors", "keywords"))
        return self


class PaperAuthorOut(BaseModel):
    author_id: UUID
    given_name: str
    surname: str
    email: str
    author_position: int
    is_corresponding: bool


class VersionOut(BaseModel):
    version_no: int
    file_location: str
    uploaded_at: datetime
    change_note: str | None


class PaperOut(BaseModel):
    paper_id: UUID
    title: str
    abstract: str
    submission_date: date
    status: str
    track_id: UUID
    track_name: str
    conference_id: UUID
    conference_acronym: str
    session_id: UUID | None
    authors: list[PaperAuthorOut]
    keywords: list[str]
    versions: list[VersionOut]


class PaperSummary(BaseModel):
    paper_id: UUID
    title: str
    status: str
    submission_date: date
    track_id: UUID
    track_name: str
    conference_id: UUID
    conference_acronym: str
    session_id: UUID | None



class ReviewCreate(BaseModel):
    paper_id: UUID
    reviewer_id: UUID
    overall_score: int = Field(ge=1, le=5)
    recommendation: Literal["accept", "reject"]
    comments_for_authors: str = Field(min_length=1)
    confidential_comments: str | None = None
    review_submission_date: date | None = None


class ReviewListItem(BaseModel):
    review_id: UUID
    paper_id: UUID
    paper_title: str
    reviewer_id: UUID
    reviewer_name: str
    overall_score: int
    recommendation: str
    review_submission_date: date


class ReviewOut(BaseModel):
    review_id: UUID
    paper_id: UUID
    reviewer_id: UUID
    overall_score: int
    recommendation: str
    comments_for_authors: str
    confidential_comments: str | None
    review_submission_date: date



class SessionCreate(BaseModel):
    conference_id: UUID
    title: str = Field(min_length=1, max_length=100)
    session_date: date
    start_time: time
    end_time: time
    room_label: str = Field(min_length=1, max_length=50)
    chair_id: UUID

    @model_validator(mode="after")
    def _times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class SessionUpdate(BaseModel):
    conference_id: UUID | None = None
    title: str | None = Field(None, min_length=1, max_length=100)
    session_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    room_label: str | None = Field(None, min_length=1, max_length=50)
    chair_id: UUID | None = None

    @model_validator(mode="after")
    def _nulls(self):
        _no_nulls(self, tuple(self.model_fields))
        return self


class SessionPaper(BaseModel):
    paper_id: UUID
    title: str
    status: str


class SessionOut(BaseModel):
    session_id: UUID
    conference_id: UUID
    title: str
    session_date: date
    start_time: time
    end_time: time
    room_label: str
    chair_id: UUID
    papers: list[SessionPaper]