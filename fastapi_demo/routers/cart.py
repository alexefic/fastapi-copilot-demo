from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Cart, Book
from ..dtos import CartAddRequest, CartInfo, BookInfo

router = APIRouter()

@router.post("/cart/add", response_model=CartInfo, summary="Add a book to the cart", description="This endpoint adds a book to the user's shopping cart and returns the updated cart information.", response_description="The updated cart's information")
def add_to_cart(cart_request: CartAddRequest = Body(...), db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.user_id == cart_request.user_id, Cart.book_id == cart_request.book_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=cart_request.user_id, book_id=cart_request.book_id, quantity=1)
        db.add(cart_item)
    db.commit()

    return get_cart_info(cart_request.user_id, db)

@router.get("/cart/{user_id}", response_model=CartInfo, summary="Get cart details", description="This endpoint retrieves the current state of the user's shopping cart.", response_description="The current cart's information")
def get_cart_info(user_id: int = Path(...), db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart not found")

    books = []
    total_price = 0.0
    for item in cart_items:
        book = db.query(Book).filter(Book.id == item.book_id).first()
        if book:
            books.append(BookInfo(book_id=book.id, title=book.title, author=book.author, pages=book.pages))
            total_price += book.price * item.quantity

    return CartInfo(user_id=user_id, books=books, total_price=total_price)
