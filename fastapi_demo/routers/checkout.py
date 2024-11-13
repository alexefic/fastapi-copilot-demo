from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Cart, Order
from ..dtos import OrderInfo, PaymentDetails

router = APIRouter()

@router.post('/checkout', response_model=OrderInfo)
def checkout(user_id: int, payment_details: PaymentDetails, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail='Cart is empty')
    # Process payment (mock implementation)
    order = Order(user_id=user_id, status='completed')
    db.add(order)
    db.commit()
    db.refresh(order)
    # Send confirmation email (mock implementation)
    send_confirmation_email(user_id, order.id)
    return OrderInfo(**order.__dict__)
