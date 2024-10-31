from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from ..database import get_db
from ..models import Book, Wishlist
from ..dtos import BookCreate, BookInfo, WishlistInfo
from ..dependencies import get_current_user
from typing import List

router = APIRouter()

@router.post('/books/', response_model=BookInfo,
             summary='Create a new book',
             description="This endpoint creates a new book with the provided details and returns the book information",
             response_description="The created book's information")
def create_book(book: BookCreate = Body(..., description='The details of the book to be created', examples={'title': 'Example Book', 'author': 'John Doe', 'year': 2021}),
                db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookInfo(**db_book.__dict__)

@router.get('/books/{book_id}',
            response_model=BookInfo,
            summary='Read a book',
            description='This endpoint retrieves the details of a book with the provided ID',
            response_description="The requested book's information")
def read_book(book_id: int = Path(..., description='The ID of the book to be retrieved', examples=1),
              db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail='Book not found')
    return BookInfo(**db_book.__dict__)

@router.put('/books/{book_id}', response_model=BookInfo)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail='Book not found')
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return BookInfo(**db_book.__dict__)

@router.delete('/books/{book_id}')
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail='Book not found')
    db.delete(db_book)
    db.commit()
    return {'message': 'Book deleted successfully'}

@router.get('/books/random', response_model=List[BookInfo])
def get_random_books_by_genre(db: Session = Depends(get_db)):
    genres = db.query(Book.genre).distinct().all()
    random_books = []
    for genre in genres:
        book = db.query(Book).filter(Book.genre == genre[0]).order_by(func.random()).first()
        if book:
            random_books.append(BookInfo(**book.__dict__))
    return random_books

@router.post('/wishlist/', response_model=WishlistInfo)
def add_to_wishlist(book_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    wishlist_item = Wishlist(user_id=user.id, book_id=book_id)
    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)
    return WishlistInfo(**wishlist_item.__dict__)
