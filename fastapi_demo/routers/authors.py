from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Author
from ..dtos import AuthorCreate, AuthorInfo

router = APIRouter()

@router.post("/authors/", response_model=AuthorInfo, status_code=201,
    summary="Create a new author",
    description="This endpoint creates a new author with the provided details and returns the author information",
    response_description="The created author's information")
def create_author(
    author: AuthorCreate = Body(..., description="The details of the author to be created"),
    db: Session = Depends(get_db)):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo.from_orm(db_author)

@router.get("/authors/{author_id}", response_model=AuthorInfo,
    summary="Read an author",
    description="This endpoint retrieves the details of an author with the provided ID",
    response_description="The requested author's information")
def read_author(
    author_id: int = Path(..., description="The ID of the author to be retrieved"),
    db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorInfo.from_orm(db_author)

@router.put("/authors/{author_id}", response_model=AuthorInfo,
    summary="Update an author",
    description="This endpoint updates the details of an author with the provided ID",
    response_description="The updated author's information")
def update_author(
    author_id: int = Path(..., description="The ID of the author to be updated"),
    author: AuthorCreate = Body(..., description="The new details of the author"),
    db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.dict().items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo.from_orm(db_author)

@router.delete("/authors/{author_id}", status_code=204,
    summary="Delete an author",
    description="This endpoint deletes an author with the provided ID",
    response_description="No content")
def delete_author(
    author_id: int = Path(..., description="The ID of the author to be deleted"),
    db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(db_author)
    db.commit()
    return
