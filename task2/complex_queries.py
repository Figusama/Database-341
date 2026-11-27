from sqlmodel import select, func, distinct, true
from database.database import engine
from backend.paper.models import paper, paper_author, paper_keyword, paper_version, review
from backend.track.models import track
from backend.user.models import app_user, author, author_research_area, reviewer, reviewer_expertise
from backend.conference.models import conference, conference_host, conference_reviewer, conference_session


full_name = app_user.given_name + " " + app_user.surname


query1 = (
    select(
        track.track_id,
        track.name,
        track.conference_id,
        func.count(distinct(paper.paper_id)).label("paper_count"),
        func.count(distinct(paper_author.author_id)).label("author_count"),
    )
    .select_from(track)
    .outerjoin(paper, paper.track_id == track.track_id)
    .outerjoin(paper_author, paper_author.paper_id == paper.paper_id)
    .group_by(track.track_id, track.name, track.conference_id)
    .order_by(track.track_id)
)


query2 = (
    select(
        reviewer.reviewer_id,
        full_name.label("full_name"),
        func.count(review.review_id).label("review_count"),
        func.avg(review.overall_score).label("avg_overall_score"),
    )
    .select_from(reviewer)
    .join(app_user, app_user.user_id == reviewer.reviewer_id)
    .outerjoin(review, review.reviewer_id == reviewer.reviewer_id)
    .group_by(reviewer.reviewer_id, app_user.given_name, app_user.surname)
    .order_by(reviewer.reviewer_id)
)


paper_counts = (
    select(
        track.conference_id,
        func.count().label("total_papers"),
        func.count().filter(paper.status == "accepted").label("accepted_papers"),
    )
    .select_from(paper)
    .join(track, track.track_id == paper.track_id)
    .group_by(track.conference_id)
    .subquery("paper_counts")
)

review_stats = (
    select(
        track.conference_id,
        func.avg(review.overall_score).label("avg_overall_score"),
    )
    .select_from(review)
    .join(paper, paper.paper_id == review.paper_id)
    .join(track, track.track_id == paper.track_id)
    .group_by(track.conference_id)
    .subquery("review_stats")
)

query3 = (
    select(
        conference.conference_id,
        conference.acronym,
        func.coalesce(paper_counts.c.total_papers, 0).label("total_papers"),
        func.coalesce(paper_counts.c.accepted_papers, 0).label("accepted_papers"),
        review_stats.c.avg_overall_score,
    )
    .select_from(conference)
    .outerjoin(paper_counts, paper_counts.c.conference_id == conference.conference_id)
    .outerjoin(review_stats, review_stats.c.conference_id == conference.conference_id)
    .order_by(conference.conference_id)
)


reviewer_counts = (
    select(
        reviewer.reviewer_id,
        func.count(review.review_id).label("review_count"),
    )
    .select_from(reviewer)
    .outerjoin(review, review.reviewer_id == reviewer.reviewer_id)
    .group_by(reviewer.reviewer_id)
    .cte("reviewer_counts")
)

overall = select(
    func.avg(reviewer_counts.c.review_count).label("avg_reviews_per_reviewer")
).cte("overall")

query4 = (
    select(
        reviewer_counts.c.reviewer_id,
        full_name.label("full_name"),
        reviewer_counts.c.review_count,
        overall.c.avg_reviews_per_reviewer,
    )
    .select_from(reviewer_counts)
    .join(app_user, app_user.user_id == reviewer_counts.c.reviewer_id)
    .join(overall, true())
    .where(reviewer_counts.c.review_count > overall.c.avg_reviews_per_reviewer)
    .order_by(reviewer_counts.c.review_count.desc(), reviewer_counts.c.reviewer_id)
)


with engine.begin() as conn:
    rows1 = conn.execute(query1).all()
    rows2 = conn.execute(query2).all()
    rows3 = conn.execute(query3).all()
    rows4 = conn.execute(query4).all()

for task, rows in [('6.1', rows1), ('6.2', rows2), ('6.3', rows3), ('6.4', rows4)]:
    print(f"\n{task}")
    for row in rows:
        print(row)