import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

np.random.seed(42)

data = pd.DataFrame({
    "patient_age": np.random.randint(18, 80, 1000),
    "claim_amount": np.random.randint(10000, 500000, 1000),
    "policy_coverage": np.random.randint(10000, 500000, 1000),
    "previous_claim_count": np.random.randint(0, 10, 1000),
})

data["status"] = np.where(
    data["claim_amount"] > data["policy_coverage"], 1, 0
)

X = data.drop("status", axis=1)
y = data["status"]

model = RandomForestClassifier()
model.fit(X, y)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "claim_model.pkl")
joblib.dump(model, MODEL_PATH)

print("Model saved at:", MODEL_PATH)