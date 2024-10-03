from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Book
from ..dtos import BookInfo

router = APIRouter()

@router.get("/search", response_model=List[BookInfo])
def search_books(isbn: str, db: Session = Depends(get_db)):
    if not isbn:
        raise HTTPException(status_code=400, detail="Please enter an ISBN")
    books = db.query(Book).filter(Book.isbn == isbn).all()
    if not books:
        raise HTTPException(status_code=404, detail="No items found")
    return [BookInfo(**book.__dict__) for book in books]