from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book, CartItem
from ..dtos import CartItemCreate, CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add")
def add_book_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == cart_item.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    cart_item_db = db.query(CartItem).filter(CartItem.book_id == cart_item.book_id).first()
    if cart_item_db:
        cart_item_db.quantity += cart_item.quantity
    else:
        cart_item_db = CartItem(book_id=cart_item.book_id, quantity=cart_item.quantity)
        db.add(cart_item_db)
    db.commit()
    db.refresh(cart_item_db)
    return {"message": "Book added to your cart", "cart": {"book_id": cart_item_db.book_id, "quantity": cart_item_db.quantity}}

@router.get("")
def view_cart(db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).all()
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    cart_response = CartResponse(
        cart_items=[CartItemInfo(book_id=item.book_id, title=item.book.title, author=item.book.author, quantity=item.quantity, price=item.book.price) for item in cart_items],
        total_price=total_price
    )
    return cart_response

@router.delete("/remove")
def remove_book_from_cart(cart_item: CartItemCreate, db: Session = Depends(get_db)):
    cart_item_db = db.query(CartItem).filter(CartItem.book_id == cart_item.book_id).first()
    if not cart_item_db:
        raise HTTPException(status_code=404, detail="Book not found in cart")
    db.delete(cart_item_db)
    db.commit()
    return {"message": "Book removed from your cart", "cart": {"book_id": cart_item_db.book_id, "quantity": cart_item_db.quantity}}
