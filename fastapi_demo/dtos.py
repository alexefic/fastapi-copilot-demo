from pydantic import BaseModel

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

class WishlistInfo(BaseModel):
    id: int
    user_id: int
    book_id: int

    class Config:
        orm_mode = True
