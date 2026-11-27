from sqlmodel import select, func, distinct, true, literal_column
from database.database import engine
from backend.paper.models import paper, paper_author, paper_keyword, paper_version, review
from backend.track.models import track
from backend.user.models import app_user, author, author_research_area, reviewer, reviewer_expertise
from backend.conference.models import conference, conference_host, conference_reviewer, conference_session


accepted_count = func.count(paper.paper_id).filter(paper.status == "accepted")
rejected_count = func.count(paper.paper_id).filter(paper.status == "rejected")
decided_count = func.count(paper.paper_id).filter(paper.status.in_(["accepted", "rejected"]))

query = (
    select(
        conference.conference_id,
        conference.acronym,
        accepted_count.label("accepted_count"),
        rejected_count.label("rejected_count"),
        func.round(
            literal_column("100.0") * accepted_count / func.nullif(decided_count, 0), 2
        ).label("acceptance_rate"),
    )
    .select_from(conference)
    .outerjoin(track, track.conference_id == conference.conference_id)
    .outerjoin(paper, paper.track_id == track.track_id)
    .group_by(conference.conference_id, conference.acronym)
    .order_by(conference.conference_id)
)

with engine.begin() as conn:
    rows = conn.execute(query).all()

for row in rows:
    print(row)

