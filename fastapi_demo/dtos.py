from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None

class PurchaseDetails(BaseModel):
    delivery_address: str
    payment_method: str

class PurchaseConfirmation(BaseModel):
    message: str
