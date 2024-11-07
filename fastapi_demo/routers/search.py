from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Book
from ..dtos import BookInfo

router = APIRouter()

@router.get("/search", response_model=List[BookInfo])
def search_books(query: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.title.ilike(f"%{query}%")).all()
    return [BookInfo(**book.__dict__) for book in books]

@router.post("/create-spotify-link")
def create_spotify_link(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Placeholder for Spotify link generation logic
    spotify_link = "https://open.spotify.com/track/xyz"
    return {"spotify_link": spotify_link}
