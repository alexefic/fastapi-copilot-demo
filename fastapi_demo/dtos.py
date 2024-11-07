from pydantic import BaseModel
from datetime import datetime

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

class DownloadRequest(BaseModel):
    book_id: int

class DownloadResponse(BaseModel):
    message: str
    book_id: int
    download_url: str

class DownloadInfo(BaseModel):
    book_id: int
    title: str
    author: str
    downloaded_at: datetime
