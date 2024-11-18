from pydantic import BaseModel

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int

    class Config:
        orm_mode = True

class ReviewCreate(BaseModel):
    review: str
    rating: int

    class Config:
        orm_mode = True