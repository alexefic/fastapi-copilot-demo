from pydantic import BaseModel
from datetime import date

class AuthorCreate(BaseModel):
    name: str
    biography: str
    birthdate: date

class AuthorInfo(BaseModel):
    id: int
    name: str
    biography: str
    birthdate: date

    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str

class BookInfo(BaseModel):
    id: int
    title: str
    author: AuthorInfo

    class Config:
        orm_mode = True
