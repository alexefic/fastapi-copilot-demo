from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Wishlist
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/wishlist")
def save_to_wishlist(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_wishlist = Wishlist(user_id=current_user.id, book_id=book_id)
    db.add(db_wishlist)
    db.commit()
    return {"message": "Book has been added to your wishlist"}
