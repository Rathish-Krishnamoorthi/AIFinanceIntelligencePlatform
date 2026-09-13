from datetime import date
from statistics import mean

from ..services.common import collection, visible_documents
from ..ml.anomaly_model import explainable_method


def suspicious_transactions():
    return [x for x in collection("transactions").find() if x.get("risk_level") in ("HIGH", "MEDIUM", "SUSPICIOUS")]


def analysis_summary():
    rows = collection("transactions").find()
    return {"analyzed": len(rows), "high_risk": sum(x.get("risk_level") == "HIGH" for x in rows), "method": explainable_method()}


def transaction_risk(transaction: dict, user: dict | None = None) -> tuple[int, str, list[str]]:
    """Return a deterministic, explainable baseline score until a trained model is configured."""
    rows = visible_documents("transactions", user) if user else collection("transactions").find()
    reasons: list[str] = []
    score = 0
    amount = float(transaction.get("amount") or 0)
    comparable = [
        float(row.get("amount") or 0) for row in rows
        if row.get("category") == transaction.get("category")
        and row.get("transaction_type") == transaction.get("transaction_type")
        and row.get("_id") != transaction.get("_id")
    ]
    if comparable:
        baseline = mean(comparable)
        if baseline and amount > baseline * 3:
            score += 40
            reasons.append("Amount is more than three times the historical category average")
    if amount >= 100000:
        score += 30
        reasons.append("Transaction exceeds the high-value review threshold")
    try:
        if date.fromisoformat(str(transaction.get("date"))) > date.today():
            score += 25
            reasons.append("Transaction date is in the future")
    except ValueError:
        score += 20
        reasons.append("Transaction date could not be validated")
    if not transaction.get("vendor_id") and transaction.get("transaction_type") == "EXPENSE":
        score += 10
        reasons.append("Expense has no vendor reference")
    level = "HIGH" if score >= 75 else "MEDIUM" if score >= 50 else "LOW"
    return min(score, 100), level, reasons or ["No unusual statistical or policy indicators detected"]
