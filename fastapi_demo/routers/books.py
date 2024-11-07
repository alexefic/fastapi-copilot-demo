from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Book, Download
from ..dtos import BookCreate, BookInfo, DownloadResponse, DownloadInfo
from datetime import datetime

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

@router.post("/books/{book_id}/download", response_model=DownloadResponse)
def download_book(book_id: int, db: Session = Depends(get_db)):
    # Check if the book exists
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Simulate download URL generation
    download_url = f"https://example.com/downloads/book_{book_id}.epub"
    
    # Log the download
    download = Download(user_id=1, book_id=book_id) # Assuming user_id is 1 for simplicity
    db.add(download)
    db.commit()
    db.refresh(download)
    
    return DownloadResponse(message="Book has been successfully downloaded", book_id=book_id, download_url=download_url)

@router.get("/books/downloads", response_model=List[DownloadInfo])
def list_downloads(db: Session = Depends(get_db)):
    downloads = db.query(Download).filter(Download.user_id == 1).all() # Assuming user_id is 1 for simplicity
    return [DownloadInfo(book_id=d.book_id, title="Example Book", author="Author Name", downloaded_at=d.downloaded_at) for d in downloads]
