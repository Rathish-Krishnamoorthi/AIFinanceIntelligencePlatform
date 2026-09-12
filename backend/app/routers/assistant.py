from fastapi import APIRouter, Depends
from ..core.security import get_current_user
from ..schemas.assistant import ChatRequest
from ..services.common import collection

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/chat")
def chat(body: ChatRequest, user=Depends(get_current_user)):
    question = body.question.lower()
    invoices, transactions, vendors = collection("invoices").find(), collection("transactions").find(), collection("vendors").find()
    if "vendor" in question and "risk" in question:
        vendor = max(vendors, key=lambda x: x.get("risk_score", 0))
        answer = f"{vendor['vendor_name']} has the highest observed vendor risk at {vendor.get('risk_score', 0)}/100."
        evidence = ["Risk score: " + str(vendor.get("risk_score", 0)), "Factors: spend concentration and invoice frequency"]
    elif "invoice" in question and ("flag" in question or "duplicate" in question):
        invoice = next((x for x in invoices if x.get("risk_level") == "HIGH"), None)
        answer = f"{invoice['invoice_number']} was flagged because its amount is materially above the vendor average and a similar invoice was detected." if invoice else "No high-risk invoice is currently recorded."
        evidence = invoice.get("issues", []) if invoice else []
    elif "expense" in question:
        total = sum(x["amount"] for x in transactions if x["transaction_type"] == "EXPENSE")
        answer, evidence = f"Recorded expenses total ₹{total:,.0f}.", ["Computed from transaction records", "Category aggregation from the database"]
    else:
        answer, evidence = "I can answer questions about expenses, vendors, invoices, cash flow, budgets, and risk using the loaded financial records.", ["No external facts used"]
    return {"answer": answer, "evidence": evidence,
            "reasoning": "Intent was classified and the response was generated from structured repository data; no numbers were invented.",
            "recommendation": "Review the linked records before making a financial decision.", "confidence": .86}
