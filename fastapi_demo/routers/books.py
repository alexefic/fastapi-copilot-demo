from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book
from ..dtos import BookInfo
from sqlalchemy.sql.expression import func
import random

router = APIRouter()

@router.get("/books/random-by-genre/")
def get_random_books_by_genre(db: Session = Depends(get_db)):
    genres = db.query(Book.genre).distinct().all()
    result = {}
    for genre_tuple in genres:
        genre = genre_tuple[0]
        books = db.query(Book).filter(Book.genre == genre).order_by(func.random()).limit(2).all()
        result[genre] = [BookInfo.from_orm(book) for book in books]
    return result
