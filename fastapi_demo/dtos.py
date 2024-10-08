from pydantic import BaseModel
from datetime import date
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None

class AuthorCreate(BaseModel):
    name: str
    biography: str
    date_of_birth: date

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    biography: Optional[str] = None
    date_of_birth: Optional[date] = None
