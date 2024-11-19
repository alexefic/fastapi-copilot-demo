from fastapi import APIRouter, Depends, HTTPException, Body, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from ..database import get_db
from ..models import Book
from ..dtos import BookCreate, BookInfo
from typing import List

router = APIRouter()

@router.post("/books/", response_model=BookInfo,
    summary="Create a new book",
    description="This endpoint creates a new book with the provided details and returns the book information",
    response_description="The created book's information")
def create_book(
    book: BookCreate = Body(..., description="The details of the book to be created", examples={"title": "Example Book", "author": "John Doe", "year": 2021}),
    db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
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

@router.put("/books/{book_id}", response_model=BookInfo)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return BookInfo(**db_book.__dict__)

@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}

@router.get("/books/search", response_model=List[BookInfo], summary="Search AI Books")
def search_books(query: str = Query(..., description="The search term to filter books by title or author"), db: Session = Depends(get_db)):
    books = db.query(Book).filter(or_(Book.title.ilike(f"%{query}%"), Book.author.ilike(f"%{query}%"))).all()
    return [BookInfo(**book.__dict__) for book in books]

@router.get("/books/filter/author", response_model=List[BookInfo], summary="Filter AI Books by Author")
def filter_books_by_author(author: str = Query(..., description="The author name to filter books by"), db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()
    return [BookInfo(**book.__dict__) for book in books]

@router.get("/books/filter/date", response_model=List[BookInfo], summary="Filter AI Books by Publication Date")
def filter_books_by_date(start_date: str = Query(..., description="The start of the publication date range (format: YYYY-MM-DD)"), end_date: str = Query(..., description="The end of the publication date range (format: YYYY-MM-DD)"), db: Session = Depends(get_db)):
    books = db.query(Book).filter(and_(Book.publication_date >= start_date, Book.publication_date <= end_date)).all()
    return [BookInfo(**book.__dict__) for book in books]
