from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book
from ..security import get_current_user
from typing import List

router = APIRouter()

@router.get("/genres/", response_model=List[str], summary="Fetch all book genres", description="This endpoint fetches all distinct book genres from the database.", response_description="A list of all book genres.")
def get_genres(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    genres = db.query(Book.genre).distinct().all()
    return [genre[0] for genre in genres]
