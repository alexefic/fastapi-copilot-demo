from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None
    isbn: Optional[str] = None

class BookSearchResponse(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    isbn: str

class AddToBasketRequest(BaseModel):
    book_id: int

class AddToBasketResponse(BaseModel):
    detail: str
