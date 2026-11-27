from pydantic import BaseModel, Field, field_validator
from uuid import UUID
import re

class res_AppUser(BaseModel):
    user_id : UUID
    given_name : str
    surname : str
    email : str
    affiliation : str
    country : str
    phone_number : str

class AuthorProfile(BaseModel):
    orcid: str | None = Field(min_length=1, max_length=20, default=None)
    area_label : str = Field(min_length=1, max_length=100)

class ReviewerProfile(BaseModel):
    years_experience: int
    area_label : str = Field(min_length=1, max_length=100)

class CreateUser(BaseModel):
    given_name : str = Field(min_length=1, max_length=50)
    surname : str = Field(min_length=1, max_length=50)
    email : str = Field(max_length=255)
    affiliation : str = Field(min_length=1, max_length=255)
    country : str = Field(min_length=1, max_length=57)
    phone_number : str = Field(min_length=1, max_length=16)
    author : AuthorProfile | None
    reviewer : ReviewerProfile | None
    @field_validator("email")
    @classmethod
    def _email(cls, v):
        v = v.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("not a valid email address")
        return v


class PatchUser(BaseModel):
    given_name : str | None = Field(min_length=1, max_length=50)
    surname : str | None = Field(min_length=1, max_length=50)
    email : str | None = Field(max_length=255)
    affiliation : str | None = Field(min_length=1, max_length=255)
    country : str | None = Field(min_length=1, max_length=57)
    phone_number : str | None = Field(min_length=1, max_length=16)
    author : AuthorProfile | None
    reviewer : ReviewerProfile | None
    @field_validator("email")
    @classmethod
    def _email(cls, v):
        v = v.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("not a valid email address")
        return v