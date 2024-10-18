from .database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    bio = Column(Text, nullable=True)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    pages = Column(Integer)
    author = relationship("Author")
