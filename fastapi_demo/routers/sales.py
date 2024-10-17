from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Book
from ..dtos import BookSalesInfo
from ..security import get_current_user, User

router = APIRouter()

@router.get("/sales/most-sold-books", response_model=List[BookSalesInfo])
def get_most_sold_books(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user.is_authenticated:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not user.has_role('business_owner'):
        raise HTTPException(status_code=403, detail="Not authorized")
    books = db.query(Book).order_by(Book.copies_sold.desc()).all()
    return [BookSalesInfo(**book.__dict__) for book in books]
