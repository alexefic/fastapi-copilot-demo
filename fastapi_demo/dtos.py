from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None

class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=1)
    biography: Optional[str] = Field(None, max_length=1000)

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
