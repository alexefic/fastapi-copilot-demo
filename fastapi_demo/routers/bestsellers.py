from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book
from typing import List

router = APIRouter()

@router.get("/bestsellers/", response_model=List[Book])
def get_bestsellers(db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.is_bestseller == True).all()

@router.get("/bestsellers/search", response_model=List[Book])
def search_bestsellers(query: str, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.is_bestseller == True, Book.title.contains(query)).all()
