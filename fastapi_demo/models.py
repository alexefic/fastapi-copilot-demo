from .database import Base
from sqlalchemy import Column, Integer, String, DateTime

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)

class PurchaseHistory(Base):
    __tablename__ = "purchase_history"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    book_id = Column(Integer, index=True)
    purchase_date = Column(DateTime)
    quantity = Column(Integer)
