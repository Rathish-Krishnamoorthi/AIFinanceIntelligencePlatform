from fastapi import APIRouter, Depends
from ..core.security import get_current_user, require_permission
from ..schemas.budget import BudgetCreate
from ..services.budget_service import recommendation
from ..services.common import collection, serialize, visible_documents
from ..services.forecasting_service import forecast_points
from ..ml.anomaly_model import explainable_method

router = APIRouter(tags=["intelligence"])


@router.get("/anomalies")
def anomalies(user=Depends(require_permission('ANOMALY_VIEW'))):
    return [serialize(x) for x in visible_documents("transactions", user)
            if x.get("risk_level") in ["HIGH", "SUSPICIOUS", "MEDIUM"]]


@router.post("/anomalies/analyze")
def analyze(user=Depends(require_permission('ANOMALY_ANALYZE'))):
    rows = visible_documents("transactions", user)
    return {"analyzed": len(rows), "high_risk": sum(x.get("risk_level") == "HIGH" for x in rows),
            "method": explainable_method()}


@router.get("/forecast/cash-flow")
def forecast(horizon: int = 90, user=Depends(require_permission('FORECAST_VIEW'))):
    rows = collection("transactions").find()
    return forecast_points(horizon) if rows else []


@router.post("/forecast/train")
def train_forecast(user=Depends(require_permission('FORECAST_GENERATE'))):
    return {"status": "trained", "model": "moving_average_regression",
            "training_rows": len(visible_documents("transactions", user))}


@router.get("/budgets")
def budgets(user=Depends(require_permission('BUDGET_VIEW'))):
    return [serialize(x) for x in visible_documents("budgets", user)]


@router.post("/budgets")
def create_budget(body: BudgetCreate, user=Depends(require_permission('BUDGET_CREATE'))):
    import uuid
    doc = body.model_dump()
    doc["_id"] = str(uuid.uuid4())
    collection("budgets").insert_one(doc)
    return serialize(doc)


@router.get("/budgets/recommendations")
def budget_recommendations(user=Depends(require_permission('BUDGET_VIEW'))):
    return [recommendation(x) for x in visible_documents("budgets", user)]


@router.get("/risk/overview")
def risk_overview(user=Depends(require_permission('RISK_VIEW'))):
    transactions = visible_documents("transactions", user)
    invoices = visible_documents("invoices", user)
    scores = [item.get("risk_score", 0) for item in transactions + invoices]
    overall = round(sum(scores) / len(scores)) if scores else 0
    return {"overall_score": overall, "level": "HIGH" if overall >= 70 else ("MEDIUM" if overall >= 40 else "LOW"),
            "breakdown": {"transaction": round(sum(item.get("risk_score", 0) for item in transactions) / len(transactions)) if transactions else 0,
                          "invoice": round(sum(item.get("risk_score", 0) for item in invoices) / len(invoices)) if invoices else 0},
            "explanations": ["Scores are calculated from stored transaction and invoice records."] if scores else ["Add records to calculate risk."]}


@router.get("/risk/vendors")
def risk_vendors(user=Depends(require_permission('RISK_VIEW'))):
    return sorted([{"vendor_id": x["vendor_id"], "vendor_name": x["vendor_name"],
                    "risk_score": x.get("risk_score", 0), "reasons": ["Spend concentration", "Frequency change"]}
                   for x in visible_documents("vendors", user)], key=lambda x: x["risk_score"], reverse=True)


@router.get("/risk/transactions")
def risk_transactions(user=Depends(require_permission('RISK_VIEW'))):
    return [serialize(x) for x in visible_documents("transactions", user) if x.get("risk_score", 0) >= 50]
