from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Author
from ..dtos import AuthorCreate, AuthorInfo
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy function to simulate admin authentication
# Replace with actual authentication logic
async def get_current_admin(token: str = Depends(oauth2_scheme)):
    if token != "admin-token":
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"username": "admin"}

@router.post("/authors/", response_model=AuthorInfo, status_code=201)
def create_author(author: AuthorCreate, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo(**db_author.__dict__)

@router.get("/authors/{author_id}", response_model=AuthorInfo)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorInfo(**db_author.__dict__)

@router.put("/authors/{author_id}", response_model=AuthorInfo)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.dict().items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return AuthorInfo(**db_author.__dict__)
