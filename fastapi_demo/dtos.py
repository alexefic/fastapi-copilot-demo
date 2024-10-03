from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    isbn: str  # Add this line

class BookInfo(BookCreate):
    id: Optional[int] = None