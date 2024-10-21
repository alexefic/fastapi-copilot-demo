from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Author
from ..dtos import AuthorCreate, AuthorInfo

router = APIRouter()

@router.post("/authors/", response_model=AuthorInfo,
    summary="Create a new author",
    description="This endpoint creates a new author with the provided details and returns the author information",
    response_description="The created author's information")
def create_author(
    author: AuthorCreate = Body(..., description="The details of the author to be created"),
    db: Session = Depends(get_db)):
    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo(**db_author.__dict__)

@router.get("/authors/", response_model=list[AuthorInfo],
    summary="Get all authors",
    description="This endpoint retrieves a list of all authors",
    response_description="A list of authors")
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).all()
    return [AuthorInfo(**author.__dict__) for author in authors]

@router.get("/authors/{author_id}", response_model=AuthorInfo,
    summary="Get an author by ID",
    description="This endpoint retrieves the details of an author with the provided ID",
    response_description="The requested author's information")
def get_author_by_id(
    author_id: int = Path(..., description="The ID of the author to be retrieved"),
    db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorInfo(**author.__dict__)
