from pydantic import BaseModel, constr
from typing import Optional

class AuthorCreate(BaseModel):
    name: constr(min_length=1)
    biography: Optional[str] = None
    other_details: Optional[str] = None

class AuthorInfo(AuthorCreate):
    id: Optional[int] = None
