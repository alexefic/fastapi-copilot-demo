from fastapi import APIRouter, Depends, HTTPException, Body, Path, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book, Wishlist
from ..dtos import BookCreate, BookInfo, WishlistCreate

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

@router.get("/books/search", response_model=BookInfo)
def search_book_by_isbn(isbn: str = Query(..., description="The ISBN of the book to be searched"), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.isbn == isbn).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookInfo(**book.__dict__)

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

@router.post("/wishlist", status_code=201)
def add_book_to_wishlist(wishlist: WishlistCreate, db: Session = Depends(get_db)):
    # Ensure the user is authenticated (pseudo-code)
    if not is_authenticated(wishlist.user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Check if the book exists
    book = db.query(Book).filter(Book.id == wishlist.book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    # Add the book to the wishlist
    db_wishlist = Wishlist(user_id=wishlist.user_id, book_id=wishlist.book_id)
    db.add(db_wishlist)
    db.commit()
    return {"detail": "Book added to wishlist"}
