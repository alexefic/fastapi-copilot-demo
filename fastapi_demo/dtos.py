from pydantic import BaseModel

class AuthorCreate(BaseModel):
    name: str
    bio: str

class AuthorInfo(BaseModel):
    id: int
    name: str
    bio: str

    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    author: AuthorCreate
    pages: int

class BookInfo(BaseModel):
    id: int
    title: str
    author: AuthorInfo
    pages: int

    class Config:
        orm_mode = True
