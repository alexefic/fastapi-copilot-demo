from pydantic import BaseModel, constr

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
        orm_mode: True

class AuthorUpdate(BaseModel):
    author: constr(min_length=1, max_length=100)
