from .database import Base
from sqlalchemy import Column, Integer, String

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)
    genre = Column(String, index=True)  # New field

class Wishlist(Base):
    __tablename__ = 'wishlist'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    book_id = Column(Integer, index=True)
