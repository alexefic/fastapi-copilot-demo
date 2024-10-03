from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book

router = APIRouter()

@router.get("/books/search")
def search_books(isbn: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.isbn == isbn).all()
    if not books:
        raise HTTPException(status_code=404, detail="No items found for the given ISBN")
    return books