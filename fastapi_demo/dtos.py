from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    biography: str
    birth_date: str
    death_date: Optional[str] = None

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    biography: Optional[str] = None
    birth_date: Optional[str] = None
    death_date: Optional[str] = None
