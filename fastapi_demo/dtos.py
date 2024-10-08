from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None

class AuthorCreate(BaseModel):
    name: str
    biography: Optional[str] = None
    other_details: Optional[str] = None

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
