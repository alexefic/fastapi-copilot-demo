from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=1)
    biography: Optional[str] = None
    other_details: Optional[str] = None

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
