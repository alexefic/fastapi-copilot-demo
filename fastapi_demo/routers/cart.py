from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_demo.database import get_db
from fastapi_demo.dtos import CartItemCreate, CartItemInfo, Cart
from fastapi_demo.models import CartItem, Book
from fastapi_demo.dependencies import get_current_user
from fastapi_demo.schemas import User

router = APIRouter()

@router.post("/cart/add", response_model=CartItemInfo)
def add_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_cart_item = CartItem(user_id=current_user.id, **cart_item.dict())
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return CartItemInfo(**db_cart_item.__dict__)

@router.get("/cart", response_model=Cart)
def view_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    books = []
    total_price = 0.0
    for item in cart_items:
        book = db.query(Book).filter(Book.id == item.book_id).first()
        books.append({
            "book_id": book.id,
            "title": book.title,
            "author": book.author,
            "quantity": item.quantity,
            "price": book.price * item.quantity
        })
        total_price += book.price * item.quantity
    return Cart(books=books, total_price=total_price)
