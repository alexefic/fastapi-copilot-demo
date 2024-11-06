from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int
    hci_number: str
    genre: str

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    hci_number: str
    genre: str

    class Config:
        orm_mode = True
