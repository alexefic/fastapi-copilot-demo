from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book, Author
from ..dtos import BookCreate, BookInfo, AuthorInfo

router = APIRouter()

@router.post("/books/", response_model=BookInfo, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == book.author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookInfo(**db_book.__dict__, author=AuthorInfo(**db_author.__dict__))

@router.get("/books/{book_id}", response_model=BookInfo)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_author = db.query(Author).filter(Author.id == db_book.author_id).first()
    return BookInfo(**db_book.__dict__, author=AuthorInfo(**db_author.__dict__))

@router.put("/books/{book_id}", response_model=BookInfo)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_author = db.query(Author).filter(Author.id == book.author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return BookInfo(**db_book.__dict__, author=AuthorInfo(**db_author.__dict__))

@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}
