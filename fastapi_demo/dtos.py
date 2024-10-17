from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int

    class Config:
        orm_mode = True

class BookSalesInfo(BaseModel):
    title: str
    author: str
    copies_sold: int
