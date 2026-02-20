import joblib
import pandas as pd
import os

model = None


def get_model():
    global model
    if model is None:
        model_path = os.path.join(os.path.dirname(__file__), "claim_model.pkl")
        model = joblib.load(model_path)
    return model


def predict_claim(claim_data: dict):
    model = get_model()

    # Convert dictionary to DataFrame
    df = pd.DataFrame([claim_data])

    # Make prediction
    prediction = model.predict(df)[0]

    # Get probability (confidence)
    if hasattr(model, "predict_proba"):
        confidence = max(model.predict_proba(df)[0])
    else:
        confidence = 0.85

    return prediction, confidence