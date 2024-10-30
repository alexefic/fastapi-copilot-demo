from .database import Base
from sqlalchemy import Column, Integer, String

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)

class TraceLog(Base):
    __tablename__ = "trace_logs"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    purchase_date = Column(String)
    buyer_id = Column(String)
