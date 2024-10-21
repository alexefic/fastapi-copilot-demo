from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    biography = Column(String)
    other_details = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
