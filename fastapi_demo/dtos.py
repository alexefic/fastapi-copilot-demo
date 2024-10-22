from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    bio: str

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None

class BookCreate(BaseModel):
    title: str
    author_id: int
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None
    author: Optional[AuthorInfo] = None
