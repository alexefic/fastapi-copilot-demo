from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    biography: str
    other_details: str

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    biography: Optional[str] = None
    other_details: Optional[str] = None
