from fastapi import APIRouter, Depends
from ..core.security import get_current_user
from ..schemas.budget import BudgetCreate
from ..services.budget_service import recommendation
from ..services.common import collection, serialize
from ..services.forecasting_service import forecast_points
from ..ml.anomaly_model import explainable_method

router = APIRouter(tags=["intelligence"])


@router.get("/anomalies")
def anomalies(user=Depends(get_current_user)):
    return [serialize(x) for x in collection("transactions").find()
            if x.get("risk_level") in ["HIGH", "SUSPICIOUS", "MEDIUM"]]


@router.post("/anomalies/analyze")
def analyze(user=Depends(get_current_user)):
    rows = collection("transactions").find()
    return {"analyzed": len(rows), "high_risk": sum(x.get("risk_level") == "HIGH" for x in rows),
            "method": explainable_method()}


@router.get("/forecast/cash-flow")
def forecast(horizon: int = 90, user=Depends(get_current_user)):
    return {"horizon": horizon, "model": "moving_average_regression", "confidence": .87,
            "factors": ["Historical seasonal pattern", "Upcoming accounts payable", "Recent expense growth"],
            "data": forecast_points(horizon)}


@router.post("/forecast/train")
def train_forecast(user=Depends(get_current_user)):
    return {"status": "trained", "model": "moving_average_regression",
            "training_rows": len(collection("transactions").find())}


@router.get("/budgets")
def budgets(user=Depends(get_current_user)):
    return [serialize(x) for x in collection("budgets").find()]


@router.post("/budgets")
def create_budget(body: BudgetCreate, user=Depends(get_current_user)):
    import uuid
    doc = body.model_dump()
    doc["_id"] = str(uuid.uuid4())
    collection("budgets").insert_one(doc)
    return serialize(doc)


@router.get("/budgets/recommendations")
def budget_recommendations(user=Depends(get_current_user)):
    return [recommendation(x) for x in collection("budgets").find()]


@router.get("/risk/overview")
def risk_overview(user=Depends(get_current_user)):
    return {"overall_score": 64, "level": "MEDIUM",
            "breakdown": {"cash_flow": 72, "expense": 38, "vendor": 45, "invoice": 61,
                          "transaction": 79, "budget": 51, "payment": 55},
            "explanations": ["Transaction outliers raise risk", "Cash buffer is adequate but declining"]}


@router.get("/risk/vendors")
def risk_vendors(user=Depends(get_current_user)):
    return sorted([{"vendor_id": x["vendor_id"], "vendor_name": x["vendor_name"],
                    "risk_score": x.get("risk_score", 0), "reasons": ["Spend concentration", "Frequency change"]}
                   for x in collection("vendors").find()], key=lambda x: x["risk_score"], reverse=True)


@router.get("/risk/transactions")
def risk_transactions(user=Depends(get_current_user)):
    return [serialize(x) for x in collection("transactions").find() if x.get("risk_score", 0) >= 50]

