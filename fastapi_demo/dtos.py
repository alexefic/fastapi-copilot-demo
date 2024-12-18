from pydantic import BaseModel
from typing import List

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    sales_volume: int
    marked_for_sale: bool

    class Config:
        orm_mode = True

class MarkBooksForSaleRequest(BaseModel):
    book_ids: List[int]
