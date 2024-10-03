from pydantic import BaseModel

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    pages: int

    class Config:
        orm_mode = True
