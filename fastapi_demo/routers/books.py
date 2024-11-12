from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Book
from ..dtos import BookCreate, BookInfo

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

@router.get("/books/search", summary="Search books by author", description="This endpoint searches for books by the specified author and returns a list of books.", response_description="A list of books by the specified author")
def search_books_by_author(author: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.author == author).all()
    return {"books": [BookInfo(**book.__dict__) for book in books]}

@router.post("/cart/buy-all", summary="Buy all searched books", description="This endpoint adds all specified books to the cart and returns a redirection URL to the checkout page.", response_description="Confirmation of books added to the cart and redirection URL to the checkout page")
def buy_all_books(book_ids: List[int], db: Session = Depends(get_db)):
    # Logic to add books to the cart
    # Assuming a Cart model and add_to_cart function exist
    for book_id in book_ids:
        add_to_cart(book_id, db)
    return {"message": "Books added to cart successfully", "redirect_url": "https://bookbridge.com/checkout"}