from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Book, BookInfo
from sqlalchemy import asc

router = APIRouter()

@router.get("/books/search", response_model=List[BookInfo])
def search_books(author: str = Query(..., description="Author's name to search for"), db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.author == author).order_by(asc(Book.title)).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found for the given author")
    return [BookInfo(**book.__dict__) for book in books]
