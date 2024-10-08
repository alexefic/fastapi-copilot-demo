from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, dtos, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/authors/", response_model=dtos.AuthorInfo, status_code=201)
def create_author(author: dtos.AuthorCreate, db: Session = Depends(get_db)):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@router.get("/authors/", response_model=List[dtos.AuthorInfo])
def get_all_authors(db: Session = Depends(get_db)):
    return db.query(models.Author).all()

@router.put("/authors/{author_id}", response_model=dtos.AuthorInfo)
def update_author(author_id: int, author: dtos.AuthorUpdate, db: Session = Depends(get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.dict(exclude_unset=True).items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return db_author
