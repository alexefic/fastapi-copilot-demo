from pydantic import BaseModel
from typing import Optional
from datetime import date

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None

class SaleInfo(BaseModel):
    id: Optional[int] = None
    book_id: int
    quantity: int
    date: date
