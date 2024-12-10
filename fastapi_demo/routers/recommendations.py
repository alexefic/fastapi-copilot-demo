from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book, PurchaseHistory
import random

router = APIRouter()

@router.post("/recommendations/")
def get_random_recommendation(user_id: int, db: Session = Depends(get_db)):
    purchase_history = db.query(PurchaseHistory).filter(PurchaseHistory.user_id == user_id).all()
    if not purchase_history:
        return {"message": "No recommendations available"}
    random_book_id = random.choice(purchase_history).book_id
    book = db.query(Book).filter(Book.id == random_book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"recommendation": {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "pages": book.pages
    }}
