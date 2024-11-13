from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Cart
from ..dtos import CartInfo

router = APIRouter()

@router.post('/cart/add', response_model=CartInfo)
def add_to_cart(book_id: int, user_id: int, db: Session = Depends(get_db)):
    cart_item = Cart(user_id=user_id, book_id=book_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return CartInfo(**cart_item.__dict__)
