from pydantic import BaseModel

class TraceLogInfo(BaseModel):
    book_id: int
    title: str
    author: str
    purchase_date: str
    buyer_id: str
