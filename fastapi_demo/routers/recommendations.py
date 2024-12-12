from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import UserBuyingHistory, Book
from ..dtos import BookInfo

router = APIRouter()

@router.get("/users/{user_id}/recommendations", response_model=List[BookInfo], summary="Get book recommendations", description="Retrieve a list of new book recommendations based on the user's previous buying history.", response_description="A list of recommended books.")
def get_recommendations(user_id: int = Path(..., description="The ID of the user to retrieve recommendations for"), db: Session = Depends(get_db)):
    user_history = db.query(UserBuyingHistory).filter(UserBuyingHistory.user_id == user_id).all()
    if not user_history:
        return {"message": "No recommendations available"}

    recommended_books = []
    for history in user_history:
        # Placeholder for recommendation logic
        recommended_books.append(
            db.query(Book).filter(Book.id != history.book_id).first()
        )

    return recommended_books
