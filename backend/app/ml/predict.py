import joblib
import pandas as pd
import os

# Load model once
model_path = os.path.join(os.path.dirname(__file__), "claim_model.pkl")
model = joblib.load(model_path)


def predict_claim(claim_data: dict):

    # Convert dictionary to DataFrame (VERY IMPORTANT)
    df = pd.DataFrame([claim_data])

    # Make prediction
    prediction = model.predict(df)[0]

    # Get probability (confidence)
    if hasattr(model, "predict_proba"):
        confidence = max(model.predict_proba(df)[0])
    else:
        confidence = 0.85  # fallback

    return prediction, confidence