from pydantic import BaseModel
from typing import Dict

class DecisionRequest(BaseModel):
    data: Dict

class DecisionResponse(BaseModel):
    decision: str
    audit_log: Dict
