from sqlmodel import select, delete, exists, and_
from database.database import engine
from backend.paper.models import paper, paper_author, paper_keyword, paper_version, review
from backend.track.models import track
from backend.user.models import app_user, author, author_research_area, reviewer, reviewer_expertise
from backend.conference.models import conference, conference_host, conference_reviewer, conference_session
full_name = app_user.given_name + " " + app_user.surname
paper_id = '00000000-0000-0000-0000-000000000401'
conference_id = '00000000-0000-0000-0000-000000000101'
query1 = (
    select(
        paper.paper_id, paper.title,
        full_name.label("corresponding_author"), app_user.email,
        track.name.label("track_name"),
        conference.conference_id, conference.acronym,
    )
    .select_from(paper)
    .join(track, track.track_id == paper.track_id)
    .join(conference, conference.conference_id == track.conference_id)
    .join(paper_author, and_(paper_author.paper_id == paper.paper_id,
                             paper_author.is_corresponding.is_(True)))
    .join(app_user, app_user.user_id == paper_author.author_id)
    .where(paper.status == "accepted")
    .order_by(paper.paper_id)
)

query2 = select(paper.paper_id, paper.title).where(paper.abstract.ilike("%machine learning%"))

query3= (
    select(paper_version.version_no, paper_version.file_location, paper_version.uploaded_at)
    .where(paper_version.paper_id == paper_id)
    .order_by(paper_version.version_no.desc())
)

query4 = (
    select(reviewer.reviewer_id, full_name.label("full_name"), app_user.email)
    .select_from(reviewer)
    .join(app_user, app_user.user_id == reviewer.reviewer_id)
    .join(conference_reviewer, conference_reviewer.reviewer_id == reviewer.reviewer_id)
    .where(
        conference_reviewer.conference_id == conference_id,
        reviewer.years_experience >= 3,
        exists().where(
            reviewer_expertise.reviewer_id == reviewer.reviewer_id,
            reviewer_expertise.area_label == "Databases",
        ),
    )
    .order_by(full_name)
    )

with engine.begin() as conn:
    rows1 = conn.execute(query1).all()
    rows2 = conn.execute(query2).all()
    rows3 = conn.execute(query3).all()
    rows4 = conn.execute(query4).all()

for task, rows in [("5.1", rows1), ("5.2", rows2), ("5.3", rows3), ("5.4", rows4)]:
    print(f"\n{task}")
    for row in rows:
        print(row)