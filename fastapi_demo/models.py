from .database import Base
from sqlalchemy import Column, Integer, String, ARRAY

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    authors = Column(ARRAY(String), index=True)
    pages = Column(Integer)
