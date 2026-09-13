from datetime import datetime
from fastapi import APIRouter, Depends
from ..core.database import store
from ..core.security import get_current_user, require_permission
from ..services.common import collection, serialize, visible_documents

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(user=Depends(require_permission('DASHBOARD_VIEW'))):
    ts, inv = visible_documents("transactions", user), visible_documents("invoices", user)
    income = sum(x["amount"] for x in ts if x["transaction_type"] == "INCOME")
    expenses = sum(x["amount"] for x in ts if x["transaction_type"] == "EXPENSE")
    pending = sum(x["total_amount"] for x in inv if x["status"] in {"PENDING", "PENDING_APPROVAL", "APPROVED"})
    paid = sum(x["total_amount"] for x in inv if x["status"] == "PAID")
    return {"total_revenue": round(income, 2), "total_expenses": round(expenses, 2),
            "net_cash_flow": round(income - expenses, 2), "accounts_payable": round(pending, 2),
            "accounts_receivable": round(sum(x["total_amount"] for x in inv if x["status"] == "APPROVED"), 2),
            "pending_invoices": sum(x["status"] in {"PENDING", "PENDING_APPROVAL"} for x in inv),
            "paid_invoices": sum(x["status"] == "PAID" for x in inv),
            "overdue_invoices": sum(x["status"] == "PENDING" and x["due_date"] < datetime.now().date().isoformat() for x in inv),
            "suspicious_transactions": sum(x.get("risk_level") in ["HIGH", "SUSPICIOUS"] for x in ts),
            "financial_risk_score": min(100, round((sum(x.get("risk_score", 0) for x in ts) / len(ts)) if ts else 0)),
            "forecasted_cash_balance": round(income - expenses - pending, 2),
            "database_mode": "demo" if store.demo_mode else "mongodb",
            "user_name": user.get("name", "Finance team")}


@router.get("/expenses")
def expenses(user=Depends(require_permission('DASHBOARD_VIEW'))):
    values = {}
    for item in visible_documents("transactions", user):
        if item["transaction_type"] == "EXPENSE":
            values[item["category"]] = values.get(item["category"], 0) + item["amount"]
    return [{"category": k, "amount": round(v, 2)} for k, v in values.items()]


@router.get("/revenue")
def revenue(user=Depends(require_permission('DASHBOARD_VIEW'))):
    grouped = {}
    for item in visible_documents("transactions", user):
        month = str(item.get("date", ""))[:7]
        if not month:
            continue
        grouped.setdefault(month, {"month": month, "revenue": 0, "expenses": 0})
        key = "revenue" if item.get("transaction_type") == "INCOME" else "expenses"
        grouped[month][key] += item.get("amount", 0)
    return [{**row, "revenue": round(row["revenue"], 2), "expenses": round(row["expenses"], 2)}
            for row in sorted(grouped.values(), key=lambda row: row["month"])]


@router.get("/cash-flow")
def cash_flow(user=Depends(require_permission('DASHBOARD_VIEW'))):
    return []


@router.get("/insights")
def insights(user=Depends(require_permission('DASHBOARD_VIEW'))):
    return [serialize(x) for x in visible_documents("notifications", user)]
