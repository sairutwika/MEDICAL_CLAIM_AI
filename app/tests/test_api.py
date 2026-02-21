from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

payload = {
    "patient_age": 40,
    "gender": "Male",
    "diagnosis_code": "D123",
    "procedure_code": "P123",
    "claim_amount": 450000,
    "policy_coverage": 300000,
    "hospital_type": "Private",
    "admission_type": "Emergency",
    "previous_claim_count": 4
}

def test_valid_claim():
    response = client.post("/submit-claim", json=payload)
    assert response.status_code == 200

def test_missing_field():
    bad_payload = payload.copy()
    bad_payload.pop("patient_age")
    response = client.post("/submit-claim", json=bad_payload)
    assert response.status_code == 422

def test_confidence_range():
    response = client.post("/submit-claim", json=payload)
    data = response.json()
    assert 0 <= data["confidence_score"] <= 1