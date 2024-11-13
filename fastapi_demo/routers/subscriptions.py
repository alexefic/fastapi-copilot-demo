from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/subscriptions/unsubscribe")
def unsubscribe_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.subscription_status == "Inactive":
        raise HTTPException(status_code=400, detail="User already unsubscribed")
    current_user.subscription_status = "Inactive"
    db.commit()
    log_unsubscribe_action(current_user.id)
    return {"message": "You have successfully unsubscribed from your monthly book subscription", "subscription_status": "Inactive"}

@router.post("/subscriptions/unsubscribe/cancel")
def cancel_unsubscribe_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.subscription_status == "Inactive":
        raise HTTPException(status_code=400, detail="User is not subscribed")
    return {"message": "You have remained subscribed", "subscription_status": "Active"}


def log_unsubscribe_action(user_id: int):
    # Implement logging logic here
    pass
