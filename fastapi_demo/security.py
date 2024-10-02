from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_admin(token: str = Depends(oauth2_scheme)) -> User:
    user = decode_token(token)  # Implement token decoding and user retrieval
    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated or not an admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
