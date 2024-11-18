from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Book
from ..dtos import BookInfo

router = APIRouter()

@router.get("/books/search", response_model=List[BookInfo])
def search_books(author_name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.author.ilike(f"%{author_name}%")).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found for the given author")
    return [BookInfo(**book.__dict__) for book in books]
