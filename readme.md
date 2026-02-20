# 🏥 AI-Based Medical Claim Processing System

An end-to-end AI-powered system that evaluates medical insurance claims, predicts approval status, detects fraud risk, and provides explainable AI-based reasoning.

---

## 🚀 Features

- Claim input validation
- Data preprocessing & encoding
- Machine Learning-based claim prediction
- Fraud risk classification (Low / Medium / High)
- Confidence score generation
- Explainable AI output
- User-based claim history storage
- FastAPI backend APIs
- Streamlit frontend interface
- Swagger/OpenAPI documentation

---

## 🧠 Machine Learning Pipeline

1. Validate structured input data
2. Encode categorical variables
3. Feature preprocessing
4. Model inference
5. Fraud risk evaluation
6. Confidence score extraction
7. Explanation generation
8. Store prediction in database

---

## 📊 Model Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

(Include your actual metric values here after training)

---

## 🏗 Architecture Overview

Frontend (Streamlit)
⬇  
FastAPI Backend
⬇  
ML Model (Scikit-learn)
⬇  
SQLite Database

---

## 🔍 Fraud Detection Logic

Fraud risk is categorized based on:

- Claim amount vs policy coverage
- Previous claim frequency
- Admission type risk
- Hospital type risk

Risk Levels:
- Low
- Medium
- High

---

## 📂 Project Structure
medical_claim_ai/
│
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── models.py
│ │ ├── database.py
│ │ ├── ml/
│ │ │ ├── train.py
│ │ │ ├── predict.py
│ │ │ ├── fraud.py
│ │ │ ├── explain.py
│ │
├── frontend/
│ ├── streamlit_app.py
│
├── requirements.txt
├── README.md