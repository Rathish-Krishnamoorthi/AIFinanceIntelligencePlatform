from fastapi import APIRouter, Depends, HTTPException
from ..core.security import require_permission
from ..services.common import audit, collection, serialize, visible_documents

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.get("")
def pending_approvals(user=Depends(require_permission('APPROVAL_VIEW'))):
    return [serialize(x) for x in visible_documents("invoices", user)
            if x.get("status") == "PENDING_APPROVAL"]


@router.post("/{item_id}/submit")
def submit_for_approval(item_id: str, user=Depends(require_permission("INVOICE_PROCESS"))):
    invoice = collection("invoices").find_one({"_id": item_id}) or collection("invoices").find_one({"invoice_number": item_id})
    if not invoice or invoice not in visible_documents("invoices", user):
        raise HTTPException(404, "Invoice not found")
    collection("invoices").update_one({"_id": invoice["_id"]}, {"$set": {"status": "PENDING_APPROVAL"}})
    audit(user, "submitted_for_approval", "invoice", invoice.get("invoice_number", item_id))
    invoice["status"] = "PENDING_APPROVAL"
    return serialize(invoice)
