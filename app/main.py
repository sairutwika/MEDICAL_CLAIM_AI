from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models
from .schemas import ClaimRequest, ClaimResponse
from .ml.predict import predict_claim
from .ml.fraud import fraud_risk_logic
from .ml.explain import generate_explanation

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Medical Claim Processing System")

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit-claim", response_model=ClaimResponse)
def submit_claim(claim: ClaimRequest, db: Session = Depends(get_db)):

    features = [
        claim.patient_age,
        claim.claim_amount,
        claim.policy_coverage,
        claim.previous_claim_count
    ]

    prediction, confidence = predict_claim(features)

    status_map = {0: "Approved", 1: "Rejected"}
    claim_status = status_map.get(prediction, "Manual Review")

    fraud_risk = fraud_risk_logic(
        claim.claim_amount,
        claim.policy_coverage,
        claim.previous_claim_count
    )

    explanation = generate_explanation(
        claim.claim_amount,
        claim.policy_coverage,
        claim.previous_claim_count
    )

    db_claim = models.Claim(
        **claim.dict(),
        claim_status=claim_status,
        fraud_risk=fraud_risk,
        confidence_score=confidence,
        explanation=explanation
    )

    db.add(db_claim)
    db.commit()

    return {
        "claim_status": claim_status,
        "fraud_risk": fraud_risk,
        "confidence_score": round(confidence, 2),
        "explanation": explanation
    }