from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    biography: str
    other_details: str

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
