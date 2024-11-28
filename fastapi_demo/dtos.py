from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None

class DownloadedBookInfo(BaseModel):
    id: int
    book_id: int
    downloaded_at: datetime
