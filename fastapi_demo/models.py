from .database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)
    reviews = relationship("Review", back_populates="book")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user = Column(String)
    rating = Column(Float)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    book = relationship("Book", back_populates="reviews")