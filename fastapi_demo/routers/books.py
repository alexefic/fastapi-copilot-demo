from fastapi import APIRouter, Depends, HTTPException, Body, Path, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book, Cart, Order
from ..dtos import BookCreate, BookInfo, CartItem, CheckoutRequest, PaymentRequest, OrderResponse

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

@router.get("/books/search", response_model=list[BookInfo], summary="Search for Romantic Sci-Fi Book")
def search_books(genre: str = Query(..., description="The genre to search for"), db: Session = Depends(get_db)):
    if genre.lower() != "romantic-sci-fi":
        raise HTTPException(status_code=400, detail="Invalid genre")
    books = db.query(Book).filter(Book.genre == genre).all()
    return [BookInfo(**book.__dict__) for book in books]

@router.post("/cart", response_model=dict, summary="Add Book to Cart")
def add_to_cart(cart_item: CartItem = Body(...), db: Session = Depends(get_db)):
    db_cart_item = Cart(**cart_item.model_dump())
    db.add(db_cart_item)
    db.commit()
    return {"message": "Book added to cart"}

@router.post("/checkout", response_model=dict, summary="Proceed to Checkout")
def proceed_to_checkout(checkout_request: CheckoutRequest = Body(...), db: Session = Depends(get_db)):
    # Here you would integrate with a delivery service and payment gateway
    payment_link = "https://paymentgateway.com/checkout/12345"
    return {"payment_link": payment_link}

@router.post("/payment/complete", response_model=OrderResponse, summary="Complete Payment")
def complete_payment(payment_request: PaymentRequest = Body(...), db: Session = Depends(get_db)):
    # Here you would verify the payment with the payment gateway
    order_id = "12345"
    delivery_date = "2023-10-04"
    return OrderResponse(order_id=order_id, delivery_date=delivery_date)
