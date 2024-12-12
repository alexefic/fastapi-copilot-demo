from pydantic import BaseModel
from typing import List, Optional

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    recommendation_reason: Optional[str] = None

    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

    class Config:
        orm_mode = True
