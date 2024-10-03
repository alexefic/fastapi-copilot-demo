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

class AuthorCreate(BaseModel):
    name: str
    biography: str
    other_details: str

class AuthorInfo(BaseModel):
    id: int
    name: str
    biography: str
    other_details: str
    book_id: int

    class Config:
        orm_mode = True