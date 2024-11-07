from .database import Base
from sqlalchemy import Column, Integer, String

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)

class AudiobookDownload(Base):
    __tablename__ = "audiobook_downloads"
    id = Column(Integer, primary_key=True, index=True)
    audiobook_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    progress = Column(Integer, default=0)
    status = Column(String, default="pending")
