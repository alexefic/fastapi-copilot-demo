from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    biography: Optional[str] = None

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None
