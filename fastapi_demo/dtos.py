from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None

class PurchaseLogCreate(BaseModel):
    book_title: str
    purchase_date: datetime
    buyer_information: str
    transaction_id: str

class PurchaseLogInfo(PurchaseLogCreate):
    id: Optional[int] = None
