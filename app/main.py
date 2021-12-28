from fastapi import FastAPI

# from . import models
# from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# Database Creation
# models.Base.metadata.create_all(bind=engine)

# FastAPI Instance Creation
app = FastAPI()

# origins = ["https://www.google.fr"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
