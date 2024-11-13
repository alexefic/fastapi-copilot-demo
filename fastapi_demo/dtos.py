from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int

class CartInfo(BaseModel):
    id: int
    user_id: int
    book_id: int

class OrderInfo(BaseModel):
    id: int
    user_id: int
    status: str

class PaymentDetails(BaseModel):
    card_number: str
    expiry_date: str
    cvv: str
