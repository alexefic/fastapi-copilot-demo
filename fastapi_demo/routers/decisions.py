from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import json
from ..database import get_db
from ..models import DecisionLog
from ..dtos import DecisionRequest, DecisionResponse

router = APIRouter()

# Service Logic

def analyze_data_and_make_decision(data):
    # Implement the decision-making logic here
    decision = "Invest in new project"  # Example decision
    return decision

@router.post("/decisions/make", response_model=DecisionResponse)
def make_decision(request: DecisionRequest, db: Session = Depends(get_db)):
    decision = analyze_data_and_make_decision(request.data)
    decision_log = DecisionLog(
        timestamp=datetime.utcnow().isoformat(),
        data_inputs=json.dumps(request.data),
        decision_criteria="Predefined criteria",
        result=decision
    )
    db.add(decision_log)
    db.commit()
    db.refresh(decision_log)
    return DecisionResponse(decision=decision, audit_log=decision_log.__dict__)
