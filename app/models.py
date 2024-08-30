from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from enum import Enum as PyEnum
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class UserRole(PyEnum):
    admin = "admin"
    author = "author"
    reader = "reader"

class User(Base):
    __tablename__ = "pragadeesh_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.reader)

class Post(Base):
    __tablename__ = "pragadeesh_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("pragadeesh_users.id"))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    author = relationship("User")

class Comment(Base):
    __tablename__ = "pragadeesh_comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("pragadeesh_posts.id"))
    user_id = Column(Integer, ForeignKey("pragadeesh_users.id"))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    user = relationship("User")
    post = relationship("Post")
