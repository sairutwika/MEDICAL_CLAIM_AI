from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
import logging

from app.database import engine, Base, SessionLocal
from app.models import User, Claim
from app.ml.predict import predict_claim
from app.ml.fraud import detect_fraud
from app.schemas import ClaimRequest

app = FastAPI()

Base.metadata.create_all(bind=engine)

# ---------------- LOGGING ----------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.get("/")
def home():
    return {"message": "Medical Claim API Running"}

# ---------------- CREATE USER ----------------
@app.post("/create_user/{username}")
def create_user(username: str, role: str = "user"):
    db: Session = SessionLocal()

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        db.close()
        return {"message": "User exists", "user_id": existing.id}

    new_user = User(username=username, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {"message": "User created", "user_id": new_user.id}

# ---------------- PREDICT ----------------
@app.post("/predict")
def predict(claim: ClaimRequest):

    db: Session = SessionLocal()

    user = db.query(User).filter(User.id == claim.user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    claim_data = claim.dict()

    prediction, confidence = predict_claim(claim_data)
    fraud_risk = detect_fraud(claim_data)

    explanation = (
        "Prediction based on claim amount and previous claim frequency."
    )

    result = {
        "claim_status": prediction,
        "fraud_risk": fraud_risk,
        "confidence_score": round(confidence, 2),
        "explanation": explanation
    }

    db_claim = Claim(
        user_id=claim.user_id,
        claim_status=prediction,
        fraud_risk=fraud_risk,
        confidence_score=confidence,
        explanation=explanation
    )

    db.add(db_claim)
    db.commit()
    db.close()

    logging.info(f"User {claim.user_id} submitted claim")

    return result

# ---------------- USER HISTORY ----------------
@app.get("/history/{user_id}")
def get_user_history(user_id: int):
    db = SessionLocal()
    claims = db.query(Claim).filter(Claim.user_id == user_id).all()
    db.close()
    return claims

# ---------------- ADMIN ALL CLAIMS ----------------
@app.get("/admin/all_claims")
def get_all_claims(user_id: int):
    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != "admin":
        db.close()
        raise HTTPException(status_code=403, detail="Access denied")

    claims = db.query(Claim).all()
    db.close()
    return claims