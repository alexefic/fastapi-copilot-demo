from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book
from ..dtos import BookInfo

router = APIRouter()

@router.get("/books/search")
def search_books(isbn: str, db: Session = Depends(get_db)):
    if not isbn:
        raise HTTPException(status_code=400, detail="Please enter an ISBN")
    book = db.query(Book).filter(Book.isbn == isbn).first()
    if book is None:
        raise HTTPException(status_code=404, detail="No results found")
    return BookInfo(**book.__dict__)