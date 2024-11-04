from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Book, Wishlist
from ..dtos import BookInfo, AddToWishlistRequest

router = APIRouter()

@router.get("/books/search", response_model=List[BookInfo])
def search_books_by_author(author: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()
    return [BookInfo.from_orm(book) for book in books]

@router.post("/wishlist")
def add_book_to_wishlist(request: AddToWishlistRequest, db: Session = Depends(get_db)):
    user_id = get_current_user_id()  # This function should retrieve the current user's ID
    db_wishlist = Wishlist(user_id=user_id, book_id=request.book_id)
    db.add(db_wishlist)
    db.commit()
    return {"message": "Book added to your wishlist"}

# Dummy function to simulate user authentication
# Replace this with actual implementation

def get_current_user_id() -> int:
    return 1  # Assuming user ID 1 for demonstration purposes
