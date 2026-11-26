from sqlmodel import select, delete, update, text, Session, insert
from database.database import engine
from sqlmodel import text, SQLModel
from backend.paper.models import paper, paper_author, paper_keyword, paper_version, review
from backend.track.models import track
from backend.user.models import app_user, author, author_research_area, reviewer, reviewer_expertise
from backend.conference.models import conference, conference_host, conference_reviewer, conference_session
from data import (app_user_rows, author_rows, author_research_area_rows, 
                  review_rows, reviewer_expertise_rows, reviewer_rows, conference_rows, 
                  conference_host_rows, conference_reviewer_rows, conference_session_rows, track_rows,
                  paper_author_rows, paper_keyword_rows, paper_rows,  paper_version_rows,
                )

with engine.begin() as conn:
    conn.execute(
        insert(app_user).values(app_user_rows)
    )
    conn.execute(
        insert(author).values(author_rows)
    )
    conn.execute(
        insert(author_research_area).values(author_research_area_rows)
    )
    conn.execute(
        insert(reviewer).values(reviewer_rows)
    )
    conn.execute(
        insert(reviewer_expertise).values(reviewer_expertise_rows)
    )
    conn.execute(
        insert(conference).values(conference_rows)
    )
    conn.execute(
        insert(conference_host).values(conference_host_rows)
    )
    conn.execute(
        insert(conference_reviewer).values(conference_reviewer_rows)
    )
    conn.execute(
        insert(track).values(track_rows)
    )
    conn.execute(
        insert(conference_session).values(conference_session_rows)
    )
    conn.execute(
        insert(paper).values(paper_rows)
    )
    conn.execute(
        insert(paper_author).values(paper_author_rows)
    )
    conn.execute(
        insert(paper_keyword).values(paper_keyword_rows)
    )
    conn.execute(
        insert(paper_version).values(paper_version_rows)
    )
    conn.execute(
        insert(review).values(review_rows)
    )

    