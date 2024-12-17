from pydantic import BaseModel
from datetime import datetime

class PurchaseHistoryDTO(BaseModel):
    customer_id: int
    book_id: int
    purchase_date: datetime
    quantity: int

    class Config:
        orm_mode = True

class TagForSaleResponse(BaseModel):
    detail: str
