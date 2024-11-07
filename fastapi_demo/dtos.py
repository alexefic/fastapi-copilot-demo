from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    genre: str

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    genre: str

class FavouriteCreate(BaseModel):
    book_id: int
