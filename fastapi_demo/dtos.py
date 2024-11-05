from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    pages: int

class BookInfo(BookCreate):
    id: Optional[int] = None

class ReviewCreate(BaseModel):
    book_id: int
    user: str
    rating: float
    comment: str

class ReviewInfo(ReviewCreate):
    id: Optional[int] = None
    created_at: datetime

class BookReviewInfo(BaseModel):
    book_id: int
    title: str
    author: str
    average_rating: float
    review_count: int