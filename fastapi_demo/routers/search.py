from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import Book
from ..dtos import BookInfo
from ..database import get_db

router = APIRouter()

@router.get("/books/search", response_model=List[BookInfo])
def search_books(category: str, db: Session = Depends(get_db)):
    if category.lower() != 'children':
        raise HTTPException(status_code=400, detail="Invalid category")
    books = db.query(Book).filter(Book.category == category).all()
    return [BookInfo(**book.__dict__) for book in books]