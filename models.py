from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DamageAssessment(BaseModel):
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    estimated_repair_cost: float
    confidence: float = Field(ge=0.0, le=1.0)


class FraudAssessment(BaseModel):
    risk_score: float = Field(ge=0.0, le=1.0)
    flags: List[str] = []
    explanation: str


class ClaimState(BaseModel):
    claim_id: str
    customer_name: str
    policy_id: str
    incident_timestamp: datetime
    incident_description: str
    vehicle_number: str

    # Updated by downstream agents
    documents_valid: bool = False
    missing_fields: List[str] = []
    damage_assessment: Optional[DamageAssessment] = None
    fraud_assessment: Optional[FraudAssessment] = None


class ClaimDecision(BaseModel):
    claim_id: str
    status: Literal["APPROVED", "REJECTED", "ESCALATED"]
    approved_amount: float
    fraud_risk_score: float
    reasons: List[str]
    customer_message: str
    audit_log_id: str
    generated_at: datetime
