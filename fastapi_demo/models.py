from .database import Base
from sqlalchemy import Column, Integer, String

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    authors = Column(String, index=True)  # Store authors as a comma-separated string
    pages = Column(Integer)
