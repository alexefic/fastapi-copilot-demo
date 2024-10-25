from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    isbn: str

class BookInfo(BookCreate):
    id: Optional[int] = None

class WishlistCreate(BaseModel):
    user_id: str
    book_id: int
