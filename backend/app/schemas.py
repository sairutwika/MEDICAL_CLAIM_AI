from pydantic import BaseModel

class ClaimRequest(BaseModel):
    user_id: int
    patient_age: int
    gender: str
    diagnosis_code: str
    procedure_code: str
    claim_amount: float
    policy_coverage_amount: float
    hospital_type: str
    admission_type: str
    previous_claim_count: int