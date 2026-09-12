def risk_level(score: float) -> str:
    return "HIGH" if score >= 75 else "MEDIUM" if score >= 50 else "LOW"
