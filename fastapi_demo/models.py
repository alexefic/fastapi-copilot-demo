from .database import Base
from sqlalchemy import Column, Integer, String

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)

class Cart(Base):
    __tablename__ = "cart"
    user_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, default=1)
