from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    genre: str

class BookInfo(BookCreate):
    id: Optional[int] = None

class CartItem(BaseModel):
    book_id: int
    quantity: int

class CheckoutRequest(BaseModel):
    address: str
    delivery_option: str

class PaymentRequest(BaseModel):
    payment_id: str
    status: str

class OrderResponse(BaseModel):
    order_id: str
    delivery_date: str
