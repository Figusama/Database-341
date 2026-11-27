from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, insert, update, delete, func
from database.database import get_session
from backend.user.schemas import res_AppUser, CreateUser, PatchUser
from backend.user.models import app_user, author, author_research_area, reviewer, reviewer_expertise
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
router = APIRouter(tags=['app_user'])


@router.get("/app_user/read/{email}", response_model=res_AppUser)
def read_user(email: str, session : Session = Depends(get_session)):
    user : app_user | None = session.exec(
        select(app_user).where(app_user.email == email)
    ).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email '{email}' not found")

    return res_AppUser(
        user_id = user.user_id,
        given_name=user.given_name,
        surname=user.surname,
        email=user.email,
        affiliation=user.affiliation,
        country=user.country,
        phone_number=user.phone_number
    )

@router.get("/app_user/read/", response_model=list[res_AppUser])
def read_users(limit : int = 100, offset : int = 0, session : Session = Depends(get_session)):
    
    users : app_user | None = session.exec(
        select(app_user)
    ).all()

    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"App User is empty")
    return [
        res_AppUser(
            user_id=user.user_id,
            given_name=user.given_name,
            surname=user.surname,
            email=user.email,
            affiliation=user.affiliation,
            country=user.country,
            phone_number=user.phone_number,
        )
        for user in users
    ]

@router.post("/app_user/create/user", status_code=status.HTTP_200_OK)
def create_user(data : CreateUser, session : Session = Depends(get_session)):

    if data.reviewer is not None:
        if data.reviewer.years_experience < 0:
            raise HTTPException(
                status_code=status.HTTP_411_LENGTH_REQUIRED,
                detail = "years_experience cannot be negative"
            )


    user_id = session.exec(
        insert(app_user).values(
            given_name=data.given_name,
            surname=data.surname,
            email=data.email,
            affiliation=data.affiliation,
            country=data.country,
            phone_number=data.phone_number,
        ).returning(app_user.user_id)
    ).scalar_one()
    if data.author is not None:
        session.exec(
            insert(author).values(
                author_id = user_id,
                orcid=data.author.orcid
            )
        )
        session.exec(
            insert(author_research_area).values(
                author_id = user_id,
                area_label=data.author.area_label
                )
        )
    if data.reviewer is not None:
        session.exec(
            insert(reviewer).values(
                reviewer_id = user_id,
                years_experience = data.reviewer.years_experience
                )
        )
        session.exec(
            insert(reviewer_expertise).values(
                reviewer_id = user_id,
                area_label=data.reviewer.area_label
            )
        )
    session.commit()
    return {"user_id": str(user_id)}

@router.patch("/app_user/{email}")
def patch_user(email: str, data: PatchUser, session: Session = Depends(get_session)):
    user = session.exec(
        select(app_user).where(func.lower(app_user.email) == email.strip().lower())
    ).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_id = user.user_id

    updates = data.model_dump(exclude_unset=True, exclude={"author", "reviewer"})
    if updates:
        session.exec(update(app_user).where(app_user.user_id == user_id).values(**updates))

    if "reviewer" in data.model_fields_set:  
        if data.reviewer is None:              
            session.exec(delete(reviewer).where(reviewer.reviewer_id == user_id))
        else:
            session.exec(
                pg_insert(reviewer)
                .values(reviewer_id=user_id, years_experience=data.reviewer.years_experience)
                .on_conflict_do_update(
                    index_elements=["reviewer_id"],
                    set_={"years_experience": data.reviewer.years_experience})
            )

    if "author" in data.model_fields_set:
        if data.author is None:
            session.exec(delete(author).where(author.author_id == user_id))
        else:
            session.exec(
                pg_insert(author)
                .values(author_id=user_id, orcid=data.author.orcid)
                .on_conflict_do_update(index_elements=["author_id"], set_={"orcid": data.author.orcid})
            )

    session.commit()
    return {"email": data.email or user.email, "message": "User updated"}

@router.delete("/app_user/{email}")
def delete_user(email: str, session: Session = Depends(get_session)):
    user = session.exec(
        select(app_user).where(func.lower(app_user.email) == email.strip().lower())
    ).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    deleted_id = str(user.user_id)
    try:
        session.delete(user)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        table = getattr(getattr(exc.orig, "diag", None), "table_name", "another table")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete this user: they are still referenced by '{table}'. "
                   "Remove those records first.",
        )

    return {"deleted": deleted_id, "email": email}


@router.get("/authors")
def list_authors(session : Session = Depends(get_session)):
    rows = session.exec(
        select(app_user).join(author, author.author_id == app_user.user_id).order_by(app_user.surname, app_user.given_name)
    ).all()
    return [
        {"author_id": a.user_id, "given_name": a.given_name, "surname": a.surname,
        "email": a.email, "affiliation": a.affiliation, "country" : a.country,
        "phone_number": a.phone_number
        }
        for a in rows
    ]

@router.get("/reviewers")
def list_reviewers(session : Session = Depends(get_session)):
    rows = session.exec(
        select(app_user).join(reviewer, reviewer.reviewer_id == app_user.user_id).order_by(app_user.surname, app_user.given_name)
    ).all()
    return [
        {"reviewers_id": a.user_id, "given_name": a.given_name, "surname": a.surname,
        "email": a.email, "affiliation": a.affiliation, "country" : a.country,
        "phone_number": a.phone_number
        }
        for a in rows
        ]
