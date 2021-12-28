from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

from sqlalchemy.sql.expression import true


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author: User

    class Config:
        orm_mode = True


class PostInsideUser(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    likes: int


class UserOut(User):
    posts: List[PostInsideUser] = []


class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., ge=0, le=1)


class Token(BaseModel):
    token: str
    type: str


class TokenPayload(BaseModel):
    id: Optional[str]
