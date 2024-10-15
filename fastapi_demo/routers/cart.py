from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Cart, CartItem, Book
from ..schemas import AddBookToCartRequest, CartResponse
from ..dependencies import get_current_user

router = APIRouter()

@router.post('/add', response_model=CartResponse)
def add_book_to_cart(request: AddBookToCartRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    book = db.query(Book).filter(Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail='Book not found')
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.book_id == request.book_id).first()
    if cart_item:
        cart_item.quantity += request.quantity
    else:
        cart_item = CartItem(cart_id=cart.id, book_id=book.id, quantity=request.quantity, price=book.price)
        db.add(cart_item)
    cart.total_price += book.price * request.quantity
    db.commit()
    db.refresh(cart)
    return {'message': 'Book has been added to your cart', 'cart': cart}

@router.get('/', response_model=CartResponse)
def view_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        return {'books': [], 'total_price': 0.0}
    return {'books': cart.items, 'total_price': cart.total_price}
