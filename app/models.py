from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import CHAR, TIMESTAMP, Boolean, Integer, String, Text
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default='true', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    user_id = Column(Integer,
                     ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False)
    author = relationship("User", backref="posts")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(CHAR(60), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text("now()"))


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer,
                     ForeignKey("posts.id", ondelete="CASCADE"),
                     primary_key=True)
    user_id = Column(Integer,
                     ForeignKey("users.id", ondelete="CASCADE"),
                     primary_key=True)
