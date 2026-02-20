from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    role = Column(String, default="user")

    claims = relationship("Claim", back_populates="user")


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    claim_status = Column(String)
    fraud_risk = Column(String)
    confidence_score = Column(Float)
    explanation = Column(String)

    user = relationship("User", back_populates="claims")