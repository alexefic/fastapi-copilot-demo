from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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

@router.get("/authors/", response_model=List[AuthorInfo])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).all()
    return [AuthorInfo(**author.__dict__) for author in authors]
