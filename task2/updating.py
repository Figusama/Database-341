from sqlmodel import select, update, case
from database.database import engine
from sqlmodel import text, SQLModel
from backend.paper.models import paper, paper_author, paper_keyword, paper_version, review
from backend.track.models import track
from backend.user.models import app_user, author, author_research_area, reviewer, reviewer_expertise
from backend.conference.models import conference, conference_host, conference_reviewer, conference_session
from datetime import timedelta
EMAIL = "arman.armanov@example.com"
CITY = 'Astana'
with engine.begin() as conn:
    # 3.1
    conn.execute(
        update(app_user).where(app_user.email == EMAIL).values(phone_number='+77773414141')
    )
    # 3.2
    conn.execute(
        update(conference).values(review_deadline=conference.review_deadline + case((conference.city == CITY, timedelta(days=7)), else_=timedelta(days=3) ))
    )
    
