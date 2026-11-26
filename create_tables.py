from database.database import engine
from sqlmodel import text, SQLModel
from backend.paper.models import paper, paper_author, paper_keyword, paper_version, review
from backend.track.models import track
from backend.user.models import app_user, author, author_research_area, reviewer, reviewer_expertise
from backend.conference.models import conference, conference_host, conference_reviewer, conference_session


with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext"))
    conn.commit()


SQLModel.metadata.create_all(engine)
