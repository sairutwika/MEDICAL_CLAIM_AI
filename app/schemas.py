from pydantic import BaseModel, Field

class ClaimRequest(BaseModel):
    patient_age: int = Field(..., gt=0)
    gender: str
    diagnosis_code: str
    procedure_code: str
    claim_amount: float
    policy_coverage: float
    hospital_type: str
    admission_type: str
    previous_claim_count: int

class ClaimResponse(BaseModel):
    claim_status: str
    fraud_risk: str
    confidence_score: float
    explanation: str