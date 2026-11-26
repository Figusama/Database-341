from datetime import date, time
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlmodel import SQLModel, Field, Column

from backend.user.models import GEN_UUID


class conference(SQLModel, table=True):
    __tablename__ = "conference"
    __table_args__ = (
        sa.CheckConstraint("end_date >= start_date", name="ck_conference_dates"),
    )
    conference_id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, server_default=GEN_UUID))
    name: str = Field(sa_column=Column(pg.VARCHAR(200), nullable=False))
    acronym: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    description: str = Field(sa_column=Column(pg.VARCHAR(400), nullable=False))
    city: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    country: str = Field(sa_column=Column(pg.VARCHAR(57), nullable=False))
    start_date: date = Field(sa_column=Column(pg.DATE, nullable=False))
    end_date: date = Field(sa_column=Column(pg.DATE, nullable=False))
    submission_deadline: date = Field(sa_column=Column(pg.DATE, nullable=False))
    review_deadline: date = Field(sa_column=Column(pg.DATE, nullable=False))


class conference_host(SQLModel, table=True):
    __tablename__ = "conference_host"
    conference_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("conference.conference_id"),
        nullable=False, primary_key=True))
    host_name: str = Field(sa_column=Column(pg.VARCHAR(200), nullable=False, primary_key=True))


class conference_reviewer(SQLModel, table=True):
    __tablename__ = "conference_reviewer"
    conference_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("conference.conference_id"),
        nullable=False, primary_key=True))
    reviewer_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("reviewer.reviewer_id", ondelete="CASCADE"),
        nullable=False, primary_key=True))


class conference_session(SQLModel, table=True):
    __tablename__ = "conference_session"
    __table_args__ = (
        sa.CheckConstraint("end_time > start_time", name="ck_session_times"),
    )
    session_id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, server_default=GEN_UUID))
    conference_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("conference.conference_id"), nullable=False))
    title: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    session_date: date = Field(sa_column=Column(pg.DATE, nullable=False))
    start_time: time = Field(sa_column=Column(pg.TIME, nullable=False))
    end_time: time = Field(sa_column=Column(pg.TIME, nullable=False))
    room_label: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    chair_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("reviewer.reviewer_id"), nullable=False))