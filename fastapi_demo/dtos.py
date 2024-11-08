from pydantic import BaseModel
from typing import List

class BookInfo(BaseModel):
    book_id: int
    title: str
    author: str
    pages: int

    class Config:
        orm_mode = True

class CartAddRequest(BaseModel):
    user_id: int
    book_id: int

class CartInfo(BaseModel):
    user_id: int
    books: List[BookInfo]
    total_price: float

    class Config:
        orm_mode = True
