def fraud_risk_logic(claim_amount, policy_coverage, previous_claim_count):

    if claim_amount > policy_coverage and previous_claim_count > 3:
        return "High"
    elif previous_claim_count >= 2:
        return "Medium"
    else:
        return "Low"