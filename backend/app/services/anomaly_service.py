from ..services.common import collection
from ..ml.anomaly_model import explainable_method


def suspicious_transactions():
    return [x for x in collection("transactions").find() if x.get("risk_level") in ("HIGH", "MEDIUM", "SUSPICIOUS")]


def analysis_summary():
    rows = collection("transactions").find()
    return {"analyzed": len(rows), "high_risk": sum(x.get("risk_level") == "HIGH" for x in rows), "method": explainable_method()}
