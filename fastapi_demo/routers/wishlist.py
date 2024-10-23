from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Wishlist
from ..dtos import WishlistCreate
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/wishlist")
def add_to_wishlist(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wishlist_item = Wishlist(user_id=current_user.id, book_id=book_id)
    db.add(wishlist_item)
    db.commit()
    return {"message": "Book added to your wishlist"}
