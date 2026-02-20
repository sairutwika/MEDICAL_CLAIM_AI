def detect_fraud(data: dict):
    score = 0

    if data["claim_amount"] > data["policy_coverage_amount"]:
        score += 2

    if data["previous_claim_count"] > 3:
        score += 2

    if data["admission_type"] == "Emergency":
        score += 1

    if score >= 4:
        return "High"
    elif score >= 2:
        return "Medium"
    else:
        return "Low"