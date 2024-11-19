from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float
import datetime

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    popularity = Column(Float, default=0.0)
