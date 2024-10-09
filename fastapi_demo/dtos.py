from pydantic import BaseModel, constr
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    isbn: constr(regex='^(97(8|9))?\d{9}(\d|X)$')

class BookInfo(BookCreate):
    id: Optional[int] = None
