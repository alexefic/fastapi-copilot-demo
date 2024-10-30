from .database import Base
from sqlalchemy import Column, Integer, String, DateTime

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)

class PurchaseLog(Base):
    __tablename__ = 'purchase_logs'
    id = Column(Integer, primary_key=True, index=True)
    book_title = Column(String, index=True)
    purchase_date = Column(DateTime)
    buyer_information = Column(String)
    transaction_id = Column(String, unique=True)
