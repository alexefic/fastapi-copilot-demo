from fastapi import Depends, HTTPException
from .database import SessionLocal
from .models import User

# Dependency to get the current user
async def get_current_user(db: SessionLocal = Depends(get_db)) -> User:
    # This is a placeholder function. Replace with actual user fetching logic.
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

class User:
    # Placeholder User class. Replace with actual User model.
    is_business_owner: bool = True
