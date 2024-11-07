from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Favourite
from ..dtos import FavouriteCreate
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/favourites", response_model=dict,
    summary="Add book to favourites",
    description="This endpoint adds a book to the user's favourites list",
    response_description="Confirmation message upon successful addition")
def add_to_favourites(
    favourite: FavouriteCreate = Body(..., description="The ID of the book to be added to favourites"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)):
    db_favourite = Favourite(user_id=user.id, book_id=favourite.book_id)
    db.add(db_favourite)
    db.commit()
    return {"message": "Book added to favourites"}
