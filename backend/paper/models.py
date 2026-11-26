from datetime import date, datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlmodel import SQLModel, Field, Column

from backend.user.models import GEN_UUID


class paper(SQLModel, table=True):
    __tablename__ = "paper"
    __table_args__ = (
        sa.CheckConstraint(
            "status IN ('submitted', 'under review', 'accepted', 'rejected', 'withdrawn')",
            name="ck_paper_status"),
    )
    paper_id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, server_default=GEN_UUID))
    track_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("track.track_id"), nullable=False))
    title: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    abstract: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    submission_date: date = Field(sa_column=Column(pg.DATE, nullable=False))
    status: str = Field(sa_column=Column(pg.VARCHAR(12), nullable=False))
    session_id: UUID | None = Field(default=None, sa_column=Column(
        pg.UUID, sa.ForeignKey("conference_session.session_id"), nullable=True))


class paper_keyword(SQLModel, table=True):
    __tablename__ = "paper_keyword"
    paper_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("paper.paper_id", ondelete="CASCADE"),
        nullable=False, primary_key=True))
    keyword: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False, primary_key=True))


class paper_author(SQLModel, table=True):
    __tablename__ = "paper_author"
    __table_args__ = (
        sa.UniqueConstraint("paper_id", "author_position", name="uq_paper_author_position"),
        sa.CheckConstraint("author_position > 0", name="ck_paper_author_position"),
    )
    paper_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("paper.paper_id", ondelete="CASCADE"),
        nullable=False, primary_key=True))
    author_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("author.author_id"),
        nullable=False, primary_key=True))
    author_position: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    is_corresponding: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False))


class paper_version(SQLModel, table=True):
    __tablename__ = "paper_version"
    __table_args__ = (
        sa.CheckConstraint("version_no > 0", name="ck_paper_version_no"),
    )
    paper_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("paper.paper_id", ondelete="CASCADE"),
        nullable=False, primary_key=True))
    version_no: int = Field(sa_column=Column(pg.INTEGER, nullable=False, primary_key=True))
    file_location: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    uploaded_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False))
    change_note: str | None = Field(default=None, sa_column=Column(pg.TEXT, nullable=True))


class review(SQLModel, table=True):
    __tablename__ = "review"
    __table_args__ = (
        sa.UniqueConstraint("paper_id", "reviewer_id", name="uq_review_paper_reviewer"),
        sa.CheckConstraint("overall_score BETWEEN 1 AND 5", name="ck_review_overall_score"),
        sa.CheckConstraint("recommendation IN ('accept', 'reject')", name="ck_review_recommendation"),
    )
    review_id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, server_default=GEN_UUID))
    paper_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("paper.paper_id", ondelete="CASCADE"), nullable=False))
    reviewer_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("reviewer.reviewer_id"), nullable=False))
    overall_score: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    recommendation: str = Field(sa_column=Column(pg.VARCHAR(6), nullable=False))
    comments_for_authors: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    confidential_comments: str | None = Field(default=None, sa_column=Column(pg.TEXT, nullable=True))
    review_submission_date: date = Field(sa_column=Column(pg.DATE, nullable=False))