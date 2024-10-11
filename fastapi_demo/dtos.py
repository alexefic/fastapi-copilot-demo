from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    biography: str
    date_of_birth: str

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None
