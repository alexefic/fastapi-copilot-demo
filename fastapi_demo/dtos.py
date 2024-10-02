from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    bio: str

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None

class BookCreate(BaseModel):
    title: str
    author: AuthorCreate
    pages: int

class BookInfo(BaseModel):
    id: Optional[int] = None
    title: str
    author: AuthorInfo
    pages: int
