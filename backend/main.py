from fastapi import FastAPI
from backend.user.router import router as user
from backend.paper.router import router as paper
from backend.paper.reviews_router import router as review
from backend.conference.router import router as session
from backend.track.router import router as track
from backend.conference.router_conference import router as conference
app = FastAPI()

app.include_router(user)
app.include_router(paper)
app.include_router(review)
app.include_router(conference)
app.include_router(session)
app.include_router(track)