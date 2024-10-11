from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Author
from ..dtos import AuthorCreate, AuthorInfo
from ..database import get_db

router = APIRouter()

@router.post("/authors/", response_model=AuthorInfo)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo(**db_author.__dict__)

@router.get("/authors/{author_id}", response_model=AuthorInfo)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorInfo(**author.__dict__)
