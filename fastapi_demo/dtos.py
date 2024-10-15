from pydantic import BaseModel
from typing import List

class AddToCartRequest(BaseModel):
    book_id: int
    quantity: int

class CartItemResponse(BaseModel):
    book_id: int
    title: str
    author: str
    quantity: int
    price: float

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_price: float
