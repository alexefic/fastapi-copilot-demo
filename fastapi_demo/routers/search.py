from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book
import re

router = APIRouter()

@router.get("/search")
def search_items(isbn: str = Query(..., min_length=10, max_length=13), db: Session = Depends(get_db)):
    # Validate ISBN format
    if not re.match(r'^(97(8|9))?\d{9}(\d|X)$', isbn):
        raise HTTPException(status_code=400, detail="Invalid ISBN format")

    # Query the database
    books = db.query(Book).filter(Book.isbn == isbn).all()
    if not books:
        raise HTTPException(status_code=404, detail="No items found")

    return books
