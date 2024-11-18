from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Book, Review
from ..dtos import BookInfo, ReviewCreate

router = APIRouter()

@router.get("/books/search", response_model=List[BookInfo])
def search_books(title: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()
    return [BookInfo(**book.__dict__) for book in books]

@router.post("/books/{book_id}/reviews")
def create_review(book_id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_review = Review(book_id=book_id, **review.dict())
    db.add(db_review)
    db.commit()
    return {"detail": "Review and rating submitted successfully"}