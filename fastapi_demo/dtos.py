from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    genre: str  # New field

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    genre: str  # New field

    class Config:
        orm_mode = True
