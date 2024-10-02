from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book, Author
from ..dtos import BookCreate, BookInfo, AuthorCreate, AuthorInfo

router = APIRouter()

@router.post("/books/", response_model=BookInfo,
    summary="Create a new book",
    description="This endpoint creates a new book with the provided details and returns the book information",
    response_description="The created book's information")
def create_book(
    book: BookCreate = Body(..., description="The details of the book to be created", examples={"title": "Example Book"}),
    db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookInfo(**db_book.__dict__)

@router.get("/books/{book_id}",
    response_model=BookInfo,
    summary="Read a book",
    description="This endpoint retrieves the details of a book with the provided ID",
    response_description="The requested book's information")
def read_book(
    book_id: int = Path(..., description="The ID of the book to be retrieved", examples=1),
    db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookInfo(**db_book.__dict__)

@router.post("/books/{book_id}/author", response_model=BookInfo,
    summary="Create author information for a book",
    description="This endpoint creates author information for a book with the provided details and returns the updated book information",
    response_description="The updated book's information")
def create_author_for_book(
    book_id: int = Path(..., description="The ID of the book to add author information to", examples=1),
    author: AuthorCreate = Body(..., description="The details of the author to be created", examples={"author_name": "John Doe", "biography": "An accomplished author", "birthdate": "1970-01-01"}),
    db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    db_book.author_id = db_author.id
    db.commit()
    db.refresh(db_book)
    return BookInfo(**db_book.__dict__)
