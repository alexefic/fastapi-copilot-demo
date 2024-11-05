from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    rating: Optional[float] = None
    price: Optional[float] = None

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    rating: Optional[float] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True
