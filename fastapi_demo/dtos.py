from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    isbn: str

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    isbn: str

    class Config:
        orm_mode = True

class WishlistCreate(BaseModel):
    user_id: str
    book_id: int
