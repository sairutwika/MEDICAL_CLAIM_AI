from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)

    patient_age = Column(Integer)
    gender = Column(String)
    diagnosis_code = Column(String)
    procedure_code = Column(String)
    claim_amount = Column(Float)
    policy_coverage = Column(Float)
    hospital_type = Column(String)
    admission_type = Column(String)
    previous_claim_count = Column(Integer)

    claim_status = Column(String)
    fraud_risk = Column(String)
    confidence_score = Column(Float)
    explanation = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)