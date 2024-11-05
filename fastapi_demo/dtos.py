from pydantic import BaseModel, constr
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    price: float
    isbn: constr(regex=r'^[0-9]{3}-[0-9]{1,5}-[0-9]{1,7}-[0-9]{1,7}-[0-9]{1}$')

class BookInfo(BookCreate):
    id: Optional[int] = None