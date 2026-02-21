import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "claim_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Model file not found. Run train.py first.")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

def predict_claim(features):
    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0].max()
    return int(prediction), float(probability)