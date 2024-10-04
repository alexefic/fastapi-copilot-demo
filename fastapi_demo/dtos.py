from pydantic import BaseModel
from typing import Optional, List

class BookCreate(BaseModel):
    title: str
    authors: List[str]  # List of authors
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    pages: Optional[int] = None
