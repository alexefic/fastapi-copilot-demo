from fastapi import APIRouter, Depends, HTTPException, Body, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Book, Review
from ..dtos import BookCreate, BookInfo, ReviewCreate, ReviewInfo, BookReviewInfo

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

@router.get("/books/{book_id}/reviews", response_model=List[ReviewInfo],
    summary="View Book Reviews",
    description="Fetches a list of reviews for a specific book",
    response_description="A list of reviews for the specified book")
def view_book_reviews(
    book_id: int = Path(..., description="The ID of the book to fetch reviews for"),
    db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    return [ReviewInfo(**review.__dict__) for review in reviews]

@router.get("/books/sort", response_model=List[BookReviewInfo],
    summary="Sort Books by Reviews",
    description="Fetches a list of books sorted by their reviews",
    response_description="A list of books sorted by their reviews")
def sort_books_by_reviews(
    sort_by: str = Query(..., description="The criteria to sort books by (e.g., reviews)", example="reviews"),
    db: Session = Depends(get_db)):
    if sort_by == "reviews":
        books = db.query(Book.id, Book.title, Book.author, func.avg(Review.rating).label('average_rating'), func.count(Review.id).label('review_count'))
                    .join(Review, Book.id == Review.book_id)
                    .group_by(Book.id)
                    .order_by(func.avg(Review.rating).desc())
                    .all()
        return [BookReviewInfo(book_id=book.id, title=book.title, author=book.author, average_rating=book.average_rating, review_count=book.review_count) for book in books]
    else:
        raise HTTPException(status_code=400, detail="Invalid sort criteria")

@router.post("/basket", response_model=dict,
    summary="Add Book to Shopping Basket",
    description="Adds a book to the user's shopping basket",
    response_description="Confirmation message")
def add_book_to_basket(
    book_id: int = Body(..., description="The ID of the book to add to the basket"),
    db: Session = Depends(get_db)):
    # Assuming we have a ShoppingBasket model and user session management
    # This is a placeholder implementation
    return {"message": "Book added to basket successfully."}