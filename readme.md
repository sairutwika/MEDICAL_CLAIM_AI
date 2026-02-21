# 🏥 AI-Based Medical Claim Processing System

An AI-powered system that evaluates medical insurance claims, predicts approval status, detects fraud risk, and provides explainable outputs.

Built using:
- FastAPI (Backend)
- Random Forest (Machine Learning)
- SQLite (Database)
- HTML/CSS/JS (Frontend)
- Pytest (Testing)

---

# 📌 1. Problem Overview

The system processes structured medical claim data and:

✔ Validates input  
✔ Cleans and processes data  
✔ Predicts claim status  
✔ Detects fraud risk  
✔ Generates explanation  
✔ Calculates confidence score  
✔ Stores claim history  
✔ Provides API + Frontend interface  

The system does NOT return raw model output without explanation.

---

# 🏗 2. System Architecture

## 🔷 High-Level Architecture
            ┌──────────────────────────┐
            │      Frontend (HTML)     │
            │  Claim Entry + Results   │
            └─────────────┬────────────┘
                          │ HTTP Request
                          ▼
            ┌──────────────────────────┐
            │       FastAPI Backend    │
            │     /submit-claim API    │
            └─────────────┬────────────┘
                          │
     ┌────────────────────┼────────────────────┐
     ▼                    ▼                    ▼

     Input Validation ML Prediction Fraud Detection
(Pydantic) (Random Forest Model) (Rule-Based)
│
▼
Explanation Generator
│
▼
SQLite Database
│
▼
JSON Response

---

# 📂 3. VS Code Project Structure

medical_claim_ai/
│
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ │
│ ├── ml/
│ │ ├── train.py
│ │ ├── predict.py
│ │ ├── fraud.py
│ │ ├── explain.py
│ │ └── claim_model.pkl
│ │
│ ├── templates/
│ │ └── index.html
│ │
│ ├── tests/
│ │ └── test_api.py
│ │
│ └── init.py
│
├── requirements.txt
├── claims.db
├── README.md

---

# 🧠 4. File Implementation Explanation

## 🔹 main.py
- Initializes FastAPI application
- Defines `/submit-claim` endpoint
- Loads ML prediction
- Calls fraud logic
- Calls explanation engine
- Saves data to database
- Returns structured response

## 🔹 database.py
- Configures SQLite connection
- Creates SQLAlchemy engine
- Manages database sessions

## 🔹 models.py
Defines database schema:

Table: `claims`
- patient_age
- gender
- diagnosis_code
- procedure_code
- claim_amount
- policy_coverage
- hospital_type
- admission_type
- previous_claim_count
- claim_status
- fraud_risk
- confidence_score
- explanation
- created_at

## 🔹 schemas.py
- Validates input using Pydantic
- Defines response model
- Ensures required fields exist

---

## 🔹 ml/train.py
- Generates synthetic dataset
- Trains RandomForestClassifier
- Saves model as `claim_model.pkl`

## 🔹 ml/predict.py
- Loads trained model
- Performs prediction
- Returns prediction + probability

## 🔹 ml/fraud.py
Implements fraud rules:

| Condition | Fraud Risk |
|-----------|------------|
| Claim > Coverage AND Previous > 3 | High |
| Previous ≥ 2 | Medium |
| Else | Low |

## 🔹 ml/explain.py
Generates human-readable explanation:
- Claim exceeds coverage
- High claim frequency
- Normal policy limits

---

## 🔹 templates/index.html
Frontend interface:
- Form inputs
- Dropdown menus
- Styled UI
- Risk color indicators
- Confidence progress bar
- Displays prediction result

---

## 🔹 tests/test_api.py
Contains automated tests:
- Valid claim submission
- Missing field validation
- Confidence score range
- Fraud risk validation

Run using:

---

# 🧠 5. Machine Learning Pipeline

1️⃣ Input Validation (Pydantic)  
2️⃣ Feature Selection  
   - patient_age  
   - claim_amount  
   - policy_coverage  
   - previous_claim_count  
3️⃣ Model Prediction (Random Forest)  
4️⃣ Fraud Risk Logic  
5️⃣ Explanation Generation  
6️⃣ Database Storage  
7️⃣ JSON Response  

---

# 📊 6. Model Evaluation

Sample performance:

- Accuracy: 0.90+
- Precision: 0.88
- Recall: 0.87
- F1 Score: 0.87

Sample Confusion Matrix:

---

# 🌐 7. API Endpoint

### POST /submit-claim

Example Input:

```json
{
  "patient_age": 50,
  "gender": "Male",
  "diagnosis_code": "D123",
  "procedure_code": "P100",
  "claim_amount": 450000,
  "policy_coverage": 300000,
  "hospital_type": "Private",
  "admission_type": "Emergency",
  "previous_claim_count": 4
}
### Example output 
{
  "claim_status": "Rejected",
  "fraud_risk": "High",
  "confidence_score": 0.87,
  "explanation": "Claim amount exceeds policy coverage. Previous claim frequency is high"
}
## swagger documentation 
http://127.0.0.1:8000/docs
## how to run 
pip install -r requirements.txt

python app/ml/train.py

uvicorn app.main:app --reload