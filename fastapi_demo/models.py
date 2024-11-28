from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)

class DownloadedBook(Base):
    __tablename__ = "downloaded_books"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    downloaded_at = Column(DateTime, default=datetime.utcnow)
