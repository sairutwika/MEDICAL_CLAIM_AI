import pandas as pd
import numpy as np

np.random.seed(42)
n = 5000

data = {
    "patient_age": np.random.randint(18, 85, n),
    "gender": np.random.choice(["Male", "Female"], n),
    "diagnosis_code": np.random.choice(["D1", "D2", "D3", "D4"], n),
    "procedure_code": np.random.choice(["P1", "P2", "P3"], n),
    "claim_amount": np.random.randint(10000, 500000, n),
    "policy_coverage_amount": np.random.randint(50000, 400000, n),
    "hospital_type": np.random.choice(["Private", "Government"], n),
    "admission_type": np.random.choice(["Emergency", "Planned"], n),
    "previous_claim_count": np.random.randint(0, 6, n)
}

df = pd.DataFrame(data)

def assign_status(row):
    if row["claim_amount"] > row["policy_coverage_amount"]:
        return "Rejected"
    elif row["previous_claim_count"] > 3:
        return "Manual Review"
    else:
        return "Approved"

df["claim_status"] = df.apply(assign_status, axis=1)

df.to_csv("claims_dataset.csv", index=False)
print("Dataset generated successfully.")