from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database import get_db
from ..models import PurchaseHistory
from ..dtos import PurchaseHistoryDTO, TagForSaleResponse

router = APIRouter()

@router.get("/purchase-history/last-month", response_model=list[PurchaseHistoryDTO],
    summary="Retrieve last month's customer purchase history",
    description="This endpoint retrieves the purchase history of customers for the last month",
    response_description="A list of purchase history records")
def get_last_month_purchase_history(db: Session = Depends(get_db)):
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    purchase_history = db.query(PurchaseHistory).filter(PurchaseHistory.purchase_date >= one_month_ago).all()
    return purchase_history

@router.post("/books/{book_id}/tag-for-sale", response_model=TagForSaleResponse,
    summary="Tag a book for sale",
    description="This endpoint tags a book for sale",
    response_description="Confirmation that the book has been tagged for sale")
def tag_book_for_sale(book_id: int = Path(..., description="The ID of the book to be tagged for sale"), db: Session = Depends(get_db)):
    # Assuming there is a 'for_sale' column in the Book model which is not shown in the provided code
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.for_sale = True
    db.commit()
    return TagForSaleResponse(detail="Book tagged for sale")
