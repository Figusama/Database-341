from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlmodel import SQLModel, Field, Column

GEN_UUID = sa.text("gen_random_uuid()")


class app_user(SQLModel, table=True):
    __tablename__ = "app_user"
    user_id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, server_default=GEN_UUID))
    given_name: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    surname: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    email: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False, unique=True))
    affiliation: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    country: str = Field(sa_column=Column(pg.VARCHAR(57), nullable=False))
    phone_number: str = Field(sa_column=Column(pg.VARCHAR(16), nullable=False))


class author(SQLModel, table=True):
    __tablename__ = "author"
    author_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("app_user.user_id", ondelete="CASCADE"),
        nullable=False, primary_key=True))
    orcid: str | None = Field(default=None, sa_column=Column(pg.VARCHAR(20), nullable=True))


class author_research_area(SQLModel, table=True):
    __tablename__ = "author_research_area"
    author_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("author.author_id", ondelete="CASCADE"),
        nullable=False, primary_key=True))
    area_label: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False, primary_key=True))


class reviewer(SQLModel, table=True):
    __tablename__ = "reviewer"
    __table_args__ = (
        sa.CheckConstraint("years_experience >= 0", name="ck_reviewer_years_experience"),
    )
    reviewer_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("app_user.user_id", ondelete="CASCADE"),
        nullable=False, primary_key=True))
    years_experience: int = Field(sa_column=Column(pg.INTEGER, nullable=False))


class reviewer_expertise(SQLModel, table=True):
    __tablename__ = "reviewer_expertise"
    reviewer_id: UUID = Field(sa_column=Column(
        pg.UUID, sa.ForeignKey("reviewer.reviewer_id", ondelete="CASCADE"),
        nullable=False, primary_key=True))
    area_label: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False, primary_key=True))