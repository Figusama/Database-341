import re
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator


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
    if not out:
        raise ValueError("at least one label is required")
    return out


def _check_email(v: str) -> str:
    v = v.strip().lower()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
        raise ValueError("not a valid email address")
    return v


class AuthorIn(BaseModel):
    orcid: str | None = Field(default=None, max_length=20)
    research_areas: list[str]

    @field_validator("orcid")
    @classmethod
    def _orcid(cls, v):
        return v.strip() or None if v else None

    @field_validator("research_areas")
    @classmethod
    def _areas(cls, v):
        return _clean_labels(v)


class ReviewerIn(BaseModel):
    years_experience: int = Field(ge=0)
    expertise: list[str]

    @field_validator("expertise")
    @classmethod
    def _expertise(cls, v):
        return _clean_labels(v)


class UserCreate(BaseModel):
    given_name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    email: str = Field(max_length=255)
    affiliation: str = Field(min_length=1, max_length=255)
    country: str = Field(min_length=1, max_length=57)
    phone_number: str = Field(min_length=1, max_length=16)
    author: AuthorIn | None = None
    reviewer: ReviewerIn | None = None

    @field_validator("email")
    @classmethod
    def _email(cls, v):
        return _check_email(v)

    @model_validator(mode="after")
    def _role(self):
        if self.author is None and self.reviewer is None:
            raise ValueError("a user must be an author, a reviewer, or both")
        return self


class UserUpdate(BaseModel):
    given_name: str | None = Field(None, min_length=1, max_length=50)
    surname: str | None = Field(None, min_length=1, max_length=50)
    email: str | None = Field(None, max_length=255)
    affiliation: str | None = Field(None, min_length=1, max_length=255)
    country: str | None = Field(None, min_length=1, max_length=57)
    phone_number: str | None = Field(None, min_length=1, max_length=16)
    author: AuthorIn | None = None
    reviewer: ReviewerIn | None = None

    @field_validator("email")
    @classmethod
    def _email(cls, v):
        return v if v is None else _check_email(v)

    @model_validator(mode="after")
    def _nulls(self):
        for f in ("given_name", "surname", "email", "affiliation", "country", "phone_number"):
            if f in self.model_fields_set and getattr(self, f) is None:
                raise ValueError(f"{f} cannot be null")
        return self


class UserListItem(BaseModel):
    user_id: UUID
    given_name: str
    surname: str
    email: str
    is_author: bool
    is_reviewer: bool


class AuthorOut(BaseModel):
    orcid: str | None
    research_areas: list[str]


class ReviewerOut(BaseModel):
    years_experience: int
    expertise: list[str]


class UserOut(BaseModel):
    user_id: UUID
    given_name: str
    surname: str
    email: str
    affiliation: str
    country: str
    phone_number: str
    author: AuthorOut | None
    reviewer: ReviewerOut | None