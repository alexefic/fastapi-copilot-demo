from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Author
from ..dtos import AuthorCreate, AuthorInfo, AuthorUpdate

router = APIRouter()

@router.post("/authors/", response_model=AuthorInfo)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo(**db_author.__dict__)

@router.get("/authors/", response_model=List[AuthorInfo])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).all()
    return [AuthorInfo(**author.__dict__) for author in authors]

@router.put("/authors/{author_id}", response_model=AuthorInfo)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.dict(exclude_unset=True).items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo(**db_author.__dict__)
