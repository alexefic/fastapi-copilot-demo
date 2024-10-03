from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book

router = APIRouter()

@router.get("/search")
def search_items(isbn: str, db: Session = Depends(get_db)):
    if not isbn:
        raise HTTPException(status_code=422, detail="Etsi paremmin, torvi")
    if len(isbn) not in [10, 13] or not isbn.isdigit():
        raise HTTPException(status_code=400, detail="Invalid ISBN")
    items = db.query(Book).filter(Book.isbn == isbn).all()
    if not items:
        raise HTTPException(status_code=404, detail="Eipä löydy")
    return items
