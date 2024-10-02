from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Author
from ..dtos import AuthorCreate, AuthorInfo

router = APIRouter()

@router.post("/books/{book_id}/authors", response_model=AuthorInfo)
def create_author(book_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(**author.dict(), book_id=book_id)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo(**db_author.__dict__)

@router.get("/books/{book_id}/authors", response_model=AuthorInfo)
def read_author(book_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.book_id == book_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorInfo(**author.__dict__)
