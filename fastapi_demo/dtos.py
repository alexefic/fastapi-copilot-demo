from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author_id: int
    pages: int

class BookInfo(BaseModel):
    id: int
    title: str
    author_id: int
    pages: int

    class Config:
        orm_mode = True

class AuthorCreate(BaseModel):
    name: str
    bio: str

class AuthorInfo(BaseModel):
    id: int
    name: str
    bio: str

    class Config:
        orm_mode = True
