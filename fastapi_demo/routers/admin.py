from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import TraceLog
from ..dtos import TraceLogInfo
from ..dependencies import get_current_admin_user

router = APIRouter()

@router.get("/admin/trace-logs", response_model=List[TraceLogInfo])
def get_trace_logs(db: Session = Depends(get_db), current_user: str = Depends(get_current_admin_user)):
    trace_logs = db.query(TraceLog).all()
    return [TraceLogInfo(**log.__dict__) for log in trace_logs]
