from pydantic import BaseModel
from typing import Optional, List

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None

class CartItemCreate(BaseModel):
    book_id: int
    quantity: int

class CartItemInfo(CartItemCreate):
    id: Optional[int] = None

class Cart(BaseModel):
    books: List[CartItemInfo]
    total_price: float
