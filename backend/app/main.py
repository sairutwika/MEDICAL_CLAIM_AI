from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import logging

from app.database import engine, Base, SessionLocal
from app.models import User, Claim
from app.ml.predict import predict_claim
from app.ml.fraud import detect_fraud
from app.schemas import ClaimRequest

app = FastAPI()

# Template configuration
templates = Jinja2Templates(directory="app/templates")


# ---------------- STARTUP EVENT ----------------
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# ---------------- LOGGING ----------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------- HOME (HTML FRONTEND) ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# ---------------- CREATE USER ----------------
@app.post("/create_user/{username}")
def create_user(username: str, role: str = "user"):
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            return {"message": "User exists", "user_id": existing.id}

        new_user = User(username=username, role=role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created", "user_id": new_user.id}
    finally:
        db.close()


# ---------------- PREDICT ----------------
@app.post("/predict")
def predict(claim: ClaimRequest):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == claim.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        claim_data = claim.dict()

        prediction, confidence = predict_claim(claim_data)
        fraud_risk = detect_fraud(claim_data)

        explanation = "Prediction based on claim amount and previous claim frequency."

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

        logging.info(f"User {claim.user_id} submitted claim")

        return result
    finally:
        db.close()


# ---------------- USER HISTORY ----------------
@app.get("/history/{user_id}")
def get_user_history(user_id: int):
    db = SessionLocal()
    try:
        claims = db.query(Claim).filter(Claim.user_id == user_id).all()
        return claims
    finally:
        db.close()


# ---------------- ADMIN ALL CLAIMS ----------------
@app.get("/admin/all_claims")
def get_all_claims(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.role != "admin":
            raise HTTPException(status_code=403, detail="Access denied")

        claims = db.query(Claim).all()
        return claims
    finally:
        db.close()