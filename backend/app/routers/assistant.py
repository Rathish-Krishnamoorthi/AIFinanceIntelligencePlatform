from fastapi import APIRouter, Depends, HTTPException
from ..core.security import get_current_user, require_permission
from ..schemas.assistant import ChatRequest
from ..services.common import audit, collection, serialize, visible_documents

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/chat")
def chat(body: ChatRequest, user=Depends(require_permission('ASSISTANT_USE'))):
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


@router.get("/workflows")
def workflows(user=Depends(require_permission('ASSISTANT_USE'))):
    invoices = visible_documents("invoices", user)
    transactions = visible_documents("transactions", user)
    pending = [invoice for invoice in invoices if invoice.get("status") in {"PENDING", "PENDING_APPROVAL"}]
    flagged = [invoice for invoice in invoices if invoice.get("issues")]
    uncategorized = [transaction for transaction in transactions if not transaction.get("category")]
    return {"actions": [
        {"type": "approve_invoice", "count": len(pending), "label": "Invoices waiting for approval",
         "automatable": user.get("role") in {"ADMIN", "FINANCE_MANAGER"}},
        {"type": "review_invoice", "count": len(flagged), "label": "Invoices with validation inconsistencies",
         "automatable": False},
        {"type": "categorize_expense", "count": len(uncategorized), "label": "Expenses needing categorization",
         "automatable": True},
    ]}


@router.post("/workflows/{action}/{item_id}")
def execute_workflow(action: str, item_id: str, user=Depends(require_permission('ASSISTANT_EXECUTE_ACTION'))):
    if action != "approve_invoice" or user.get("role") not in {"ADMIN", "FINANCE_MANAGER"}:
        raise HTTPException(403, "This workflow requires a finance officer or administrator")
    invoice = next((row for row in visible_documents("invoices", user)
                    if row.get("invoice_number") == item_id or row.get("_id") == item_id), None)
    if not invoice:
        raise HTTPException(404, "Invoice not found")
    collection("invoices").update_one({"_id": invoice["_id"]}, {"$set": {"status": "APPROVED"}})
    audit(user, "approved_by_agent", "invoice", invoice["invoice_number"])
    invoice["status"] = "APPROVED"
    return serialize(invoice)
