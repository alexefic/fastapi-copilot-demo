from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..models import PurchaseLog
from ..dtos import PurchaseLogInfo
from ..database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def get_current_admin(token: str = Security(oauth2_scheme)):
    # Implement admin authentication and authorization logic here
    pass

@router.get('/admin/trace-logs', response_model=List[PurchaseLogInfo])
async def get_trace_logs(db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    trace_logs = db.query(PurchaseLog).all()
    return [PurchaseLogInfo(**log.__dict__) for log in trace_logs]
