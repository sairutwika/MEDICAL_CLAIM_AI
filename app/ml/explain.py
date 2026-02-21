def generate_explanation(claim_amount, policy_coverage, previous_claim_count):

    reasons = []

    if claim_amount > policy_coverage:
        reasons.append("Claim amount exceeds policy coverage")

    if previous_claim_count > 3:
        reasons.append("Previous claim frequency is high")

    if not reasons:
        reasons.append("Claim within normal policy limits")

    return ". ".join(reasons)