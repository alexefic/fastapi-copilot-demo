from pydantic import BaseModel
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
    other_details: str

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    biography: Optional[str] = None
    other_details: Optional[str] = None
