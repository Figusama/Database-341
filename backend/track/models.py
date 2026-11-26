from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlmodel import SQLModel, Field, Column

from backend.user.models import GEN_UUID


class track(SQLModel, table=True):
    __tablename__ = "track"
    track_id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, server_default=GEN_UUID))
    conference_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("conference.conference_id"), nullable=False))
    name: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    description: str = Field(sa_column=Column(pg.VARCHAR(400), nullable=False))
    research_area: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    coordinator_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("reviewer.reviewer_id"), nullable=False))