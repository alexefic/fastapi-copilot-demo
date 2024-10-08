from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Author, Book
from ..dtos import AuthorCreate, AuthorInfo

router = APIRouter()

@router.post("/books/{book_id}/authors", response_model=AuthorInfo, status_code=201)
def create_author(book_id: int, author: AuthorCreate = Body(...), db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_author = Author(**author.dict(), book_id=book_id)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo.from_orm(db_author)

@router.get("/books/{book_id}/authors", response_model=AuthorInfo)
def get_author(book_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.book_id == book_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorInfo.from_orm(db_author)
