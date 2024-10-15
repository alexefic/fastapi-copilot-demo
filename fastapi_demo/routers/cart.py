from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import CartItem, Book
from ..database import get_db
from ..dtos import AddToCartRequest, CartResponse, CartItemResponse
from ..dependencies import get_current_user, User

router = APIRouter()

@router.post('/cart/add', response_model=CartResponse)
def add_to_cart(request: AddToCartRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail='Book not found')
    cart_item = db.query(CartItem).filter(CartItem.user_id == current_user.id, CartItem.book_id == request.book_id).first()
    if cart_item:
        cart_item.quantity += request.quantity
    else:
        cart_item = CartItem(user_id=current_user.id, book_id=request.book_id, quantity=request.quantity, price=book.price)
        db.add(cart_item)
    db.commit()
    return get_cart_response(db, current_user.id)

@router.get('/cart', response_model=CartResponse)
def view_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_cart_response(db, current_user.id)

def get_cart_response(db: Session, user_id: int) -> CartResponse:
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    items = [CartItemResponse(book_id=item.book_id, title=item.book.title, author=item.book.author, quantity=item.quantity, price=item.price) for item in cart_items]
    total_price = sum(item.price * item.quantity for item in cart_items)
    return CartResponse(items=items, total_price=total_price)
