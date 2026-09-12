from datetime import datetime
from fastapi import APIRouter, Depends
from ..core.database import store
from ..core.security import get_current_user
from ..services.common import collection, serialize

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(user=Depends(get_current_user)):
    ts, inv = collection("transactions").find(), collection("invoices").find()
    income = sum(x["amount"] for x in ts if x["transaction_type"] == "INCOME")
    expenses = sum(x["amount"] for x in ts if x["transaction_type"] == "EXPENSE")
    pending = sum(x["total_amount"] for x in inv if x["status"] == "PENDING")
    paid = sum(x["total_amount"] for x in inv if x["status"] == "PAID")
    return {"total_revenue": round(income, 2), "total_expenses": round(expenses, 2),
            "net_cash_flow": round(income - expenses, 2), "accounts_payable": round(pending, 2),
            "accounts_receivable": round(income * .22, 2),
            "pending_invoices": sum(x["status"] == "PENDING" for x in inv),
            "paid_invoices": sum(x["status"] == "PAID" for x in inv),
            "overdue_invoices": sum(x["status"] == "PENDING" and x["due_date"] < datetime.now().date().isoformat() for x in inv),
            "suspicious_transactions": sum(x.get("risk_level") in ["HIGH", "SUSPICIOUS"] for x in ts),
            "financial_risk_score": 64, "forecasted_cash_balance": round((income - expenses) * .17 + pending, 2),
            "database_mode": "demo" if store.demo_mode else "mongodb"}


@router.get("/expenses")
def expenses(user=Depends(get_current_user)):
    values = {}
    for item in collection("transactions").find():
        if item["transaction_type"] == "EXPENSE":
            values[item["category"]] = values.get(item["category"], 0) + item["amount"]
    return [{"category": k, "amount": round(v, 2)} for k, v in values.items()]


@router.get("/revenue")
def revenue(user=Depends(get_current_user)):
    return [{"month": f"M-{i:02}", "revenue": 100000 + i * 3200,
             "expenses": 72000 + i * 4100, "profit": 28000 - i * 900} for i in range(1, 13)]


@router.get("/cash-flow")
def cash_flow(user=Depends(get_current_user)):
    return [{"date": f"D-{i:02}", "actual": 850000 + i * 2200 if i < 15 else None,
             "forecast": 880000 + i * 2500, "lower": 830000 + i * 1800,
             "upper": 930000 + i * 3200} for i in range(1, 31)]


@router.get("/insights")
def insights(user=Depends(get_current_user)):
    return [serialize(x) for x in collection("notifications").find()]
