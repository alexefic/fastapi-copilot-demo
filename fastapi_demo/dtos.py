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

class BuyAllBooksRequest(BaseModel):
    book_ids: List[int]