from pydantic import BaseModel
from typing import List

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int

    class Config:
        orm_mode = True

class AddToWishlistRequest(BaseModel):
    book_id: int
