from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    biography: str
    birth_date: str
    death_date: Optional[str] = None

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None
