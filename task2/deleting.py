from sqlmodel import select, delete, exists
from database.database import engine
from backend.paper.models import paper, paper_author, paper_keyword, paper_version, review
from backend.track.models import track
from backend.user.models import app_user, author, author_research_area, reviewer, reviewer_expertise
from backend.conference.models import conference, conference_host, conference_reviewer, conference_session

with engine.connect() as conn:
    #4.1
    target_1 = (
        select(paper.paper_id).join(paper_author, paper_author.paper_id == paper.paper_id)
        .join(app_user, app_user.user_id == paper_author.author_id)
        .where(paper.status == "withdrawn",paper_author.is_corresponding.is_(True), app_user.email == "amina.aminova@example.com")
    )

    before = conn.execute(
        select(paper)
    ).all()
    after = conn.execute(
        delete(paper).where(paper.paper_id.in_(target_1)).returning(paper)
    ).all()
    print("\n7")
    print("BEFORE:", before)
    print("AFTER:", after)
    print("\n7")
    #4.2
    before = conn.execute(
        select(conference_session)
    ).all()
    after = conn.execute(
        delete(conference_session).where(
        conference_session.conference_id.in_( select(conference.conference_id).where(conference.city == 'Astana') ),
        ~exists().where(paper.session_id == conference_session.session_id)).returning(conference_session)
        ).all()
    print("\n7")
    print("BEFORE:", before)
    print("AFTER:", after)
    print("\n7")

conn.rollback()
   