from sqlmodel import select, delete, exists, and_, table, column, text
from sqlalchemy.orm import aliased
from sqlalchemy.dialects import postgresql as pg
from database.database import engine
from backend.paper.models import paper, paper_author, paper_keyword, paper_version, review
from backend.track.models import track
from backend.user.models import app_user, author, author_research_area, reviewer, reviewer_expertise
from backend.conference.models import conference, conference_host, conference_reviewer, conference_session

chair = aliased(app_user)
corresponding = aliased(app_user)

view_query = (
    select(
        paper.paper_id,
        paper.title.label("paper_title"),
        conference.conference_id,
        conference.acronym,
        track.name.label("track_name"),
        conference_session.session_id,
        conference_session.title.label("session_title"),
        conference_session.session_date,
        conference_session.start_time,
        conference_session.end_time,
        conference_session.room_label,
        (chair.given_name + " " + chair.surname).label("chair_name"),
        (corresponding.given_name + " " + corresponding.surname).label("corresponding_author_name"),
        corresponding.email.label("corresponding_author_email"),
    )
    .select_from(paper)
    .join(conference_session, conference_session.session_id == paper.session_id)
    .join(conference, conference.conference_id == conference_session.conference_id)
    .join(track, track.track_id == paper.track_id)
    .join(chair, chair.user_id == conference_session.chair_id)
    .join(paper_author, (paper_author.paper_id == paper.paper_id) & paper_author.is_corresponding.is_(True))
    .join(corresponding, corresponding.user_id == paper_author.author_id)
)

create_view_sql = (
    "CREATE OR REPLACE VIEW accepted_paper_schedule AS "
    + str(view_query.compile(dialect=pg.dialect(), compile_kwargs={"literal_binds": True}))
)


accepted_paper_schedule = table(
    "accepted_paper_schedule",
    column("paper_id"), column("paper_title"),
    column("conference_id"), column("acronym"), column("track_name"),
    column("session_id"), column("session_title"), column("session_date"),
    column("start_time"), column("end_time"), column("room_label"),
    column("chair_name"), column("corresponding_author_name"), column("corresponding_author_email"),
)

query = select(accepted_paper_schedule).order_by(
    accepted_paper_schedule.c.conference_id,
    accepted_paper_schedule.c.session_date,
    accepted_paper_schedule.c.start_time,
    accepted_paper_schedule.c.session_id,
    accepted_paper_schedule.c.paper_id,
)

with engine.begin() as conn:
    conn.execute(text(create_view_sql))
    rows = conn.execute(query).all()

print("\n8")
for row in rows:
    print(row)