from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Author
from ..dtos import AuthorCreate, AuthorInfo

router = APIRouter()

@router.post("/authors/", response_model=AuthorInfo)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    if not author.name:
        raise HTTPException(status_code=400, detail="Field 'name' is required")
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo.from_orm(db_author)

@router.get("/authors/{author_id}", response_model=AuthorInfo)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorInfo.from_orm(db_author)

@router.put("/authors/{author_id}", response_model=AuthorInfo)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.dict().items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo.from_orm(db_author)
