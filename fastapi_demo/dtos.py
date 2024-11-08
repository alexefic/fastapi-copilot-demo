from pydantic import BaseModel
from typing import Optional, List

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    price: float

class BookInfo(BookCreate):
    id: Optional[int] = None

class CartItemCreate(BaseModel):
    book_id: int
    quantity: int

class CartItemInfo(BaseModel):
    book_id: int
    title: str
    author: str
    quantity: int
    price: float

class CartResponse(BaseModel):
    cart_items: List[CartItemInfo]
    total_price: float
