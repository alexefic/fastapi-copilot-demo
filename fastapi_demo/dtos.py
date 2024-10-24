from pydantic import BaseModel, validator
import re

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    isbn: str

    @validator('isbn')
    def validate_isbn(cls, v):
        if not re.match(r'^(97(8|9))?\d{9}(\d|X)$', v):
            raise ValueError('Invalid ISBN')
        return v

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    isbn: str

    class Config:
        orm_mode = True
