from pydantic import BaseModel

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    genre: str

    class Config:
        orm_mode = True
