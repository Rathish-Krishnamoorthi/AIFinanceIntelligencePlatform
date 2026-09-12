import re
import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from ..core.security import get_current_user
from ..services.common import audit, collection, serialize
from ..services.invoice_service import find_invoice
from ..utils.invoice_parser import extract_total

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("")
def list_invoices(status: Optional[str] = None, user=Depends(get_current_user)):
    return [serialize(x) for x in collection("invoices").find({"status": status} if status else {})]


@router.get("/{item_id}")
def get_invoice(item_id: str, user=Depends(get_current_user)):
    found = find_invoice(item_id)
    if not found: raise HTTPException(404, "Invoice not found")
    return serialize(found)


@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...), user=Depends(get_current_user)):
    if file.content_type not in {"application/pdf", "image/jpeg", "image/png"}:
        raise HTTPException(415, "Only PDF, JPG, and PNG invoices are supported")
    data = await file.read()
    if len(data) > 10 * 1024 * 1024: raise HTTPException(413, "Invoice must be smaller than 10 MB")
    text = data[:100000].decode("utf-8", "ignore") if file.content_type != "application/pdf" else ""
    amount = extract_total(text)
    doc = {"_id": str(uuid.uuid4()), "invoice_number": f"UPLOAD-{uuid.uuid4().hex[:6].upper()}",
           "vendor_name": "Uploaded vendor", "vendor_id": "VEN-UPLOAD",
           "invoice_date": datetime.now().date().isoformat(), "due_date": datetime.now().date().isoformat(),
           "subtotal": round(amount * .9, 2), "tax": round(amount * .1, 2), "discount": 0,
           "total_amount": amount, "currency": "INR", "status": "PENDING_APPROVAL",
           "confidence_score": .78 if not text else .91, "risk_level": "MEDIUM", "risk_score": 45,
           "issues": [], "source_filename": file.filename}
    collection("invoices").insert_one(doc)
    audit(user, "uploaded", "invoice", doc["invoice_number"])
    return serialize(doc)


def _invoice_action(item_id, status, user):
    doc = find_invoice(item_id)
    if not doc: raise HTTPException(404, "Invoice not found")
    collection("invoices").update_one({"_id": doc["_id"]}, {"$set": {"status": status}})
    audit(user, status.lower(), "invoice", doc["invoice_number"])
    doc["status"] = status
    return serialize(doc)


@router.post("/{item_id}/approve")
def approve_invoice(item_id: str, user=Depends(get_current_user)):
    return _invoice_action(item_id, "APPROVED", user)


@router.post("/{item_id}/reject")
def reject_invoice(item_id: str, user=Depends(get_current_user)):
    return _invoice_action(item_id, "REJECTED", user)
