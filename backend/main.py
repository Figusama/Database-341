from fastapi import FastAPI
from backend.user.router import router as user
from backend.paper.router import router as paper
from backend.paper.reviews_router import router as review
from backend.conference.router import router as session

app = FastAPI()

app.include_router(user)
app.include_router(paper)
app.include_router(review)
app.include_router(session)