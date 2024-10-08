from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, dtos
from ..database import get_db

router = APIRouter()

@router.post("/authors/", response_model=dtos.AuthorInfo)
def create_author(author: dtos.AuthorCreate, db: Session = Depends(get_db)):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return {**db_author.__dict__, "message": "Author information has been successfully saved"}

@router.get("/authors/", response_model=List[dtos.AuthorInfo])
def read_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return authors

@router.put("/authors/{author_id}", response_model=dtos.AuthorInfo)
def update_author(author_id: int, author: dtos.AuthorUpdate, db: Session = Depends(get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.dict(exclude_unset=True).items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return {**db_author.__dict__, "message": "Author information has been successfully updated"}
