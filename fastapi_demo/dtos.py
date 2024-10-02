from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    biography: str
    other_details: str

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None
    book_id: Optional[int] = None
