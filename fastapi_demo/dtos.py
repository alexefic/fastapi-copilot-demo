from pydantic import BaseModel, constr

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    isbn: constr(regex=r'^(97(8|9))?\d{9}(\d|X)$')  # ISBN-10 or ISBN-13 validation

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    isbn: str

    class Config:
        orm_mode = True
