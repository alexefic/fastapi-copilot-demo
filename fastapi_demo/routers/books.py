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
    book: BookCreate = Body(..., description="The details of the book to be created", examples={"title": "Example Book", "author": {"name": "John Doe", "bio": "Author bio"}, "pages": 2021}),
    db: Session = Depends(get_db)):
    db_author = Author(name=book.author.name, bio=book.author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    db_book = Book(title=book.title, author_id=db_author.id, pages=book.pages)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookInfo(id=db_book.id, title=db_book.title, author=AuthorInfo(id=db_author.id, name=db_author.name, bio=db_author.bio), pages=db_book.pages)

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
    db_author = db.query(Author).filter(Author.id == db_book.author_id).first()
    return BookInfo(id=db_book.id, title=db_book.title, author=AuthorInfo(id=db_author.id, name=db_author.name, bio=db_author.bio), pages=db_book.pages)
