import base64
import hashlib
import io
import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field
from ..core.security import get_current_user, require_permission, require_roles
from ..services.common import audit, collection, department_for, refresh_vendor, serialize, sync_vendor_for_transaction, visible_documents
from ..services.invoice_service import find_invoice
from ..services.ocr_service import extract_invoice_text
from ..utils.invoice_parser import extract_field, extract_total

router = APIRouter(prefix="/invoices", tags=["invoices"])


class InvoiceReview(BaseModel):
    invoice_number: str | None = None
    vendor_id: str | None = None
    vendor_name: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None
    subtotal: float | None = Field(default=None, ge=0)
    tax: float | None = Field(default=None, ge=0)
    discount: float | None = Field(default=None, ge=0)
    total_amount: float | None = Field(default=None, ge=0)
    currency: str | None = None
    line_items: list[dict] | None = None
    gstin: str | None = None
    purchase_order_number: str | None = None


class PaymentRequest(BaseModel):
    amount: float = Field(gt=0)
    payment_method: str = "Bank transfer"
    reference: str | None = None


@router.get("")
def list_invoices(status: Optional[str] = None, user=Depends(require_permission('INVOICE_VIEW'))):
    rows = visible_documents("invoices", user)
    if status:
        rows = [row for row in rows if row.get("status") == status]
    return [invoice_response(x) for x in rows]


def _visible_invoice(item_id, user):
    doc = find_invoice(item_id)
    if not doc:
        raise HTTPException(404, "Invoice not found")
    if doc.get("organization_id") and user.get("organization_id") != doc.get("organization_id"):
        raise HTTPException(404, "Invoice not found")
    if user.get("canonical_role") == "EMPLOYEE" and doc.get("user_id") != user.get("id"):
        raise HTTPException(404, "Invoice not found")
    if not can_manage_invoice(user) and doc.get("department") and doc.get("department") != user.get("department"):
        raise HTTPException(404, "Invoice not found")
    return doc


def can_manage_invoice(user):
    return user.get("canonical_role") in {"FINANCE_MANAGER", "CFO"}


def invoice_response(document):
    result = serialize(document)
    if result:
        result.pop("file_content", None)
    return result


@router.get("/{item_id}")
def get_invoice(item_id: str, user=Depends(require_permission('INVOICE_VIEW'))):
    return invoice_response(_visible_invoice(item_id, user))


@router.patch("/{item_id}")
def review_invoice(item_id: str, body: InvoiceReview,
                   user=Depends(require_permission('INVOICE_UPDATE'))):
    doc = _visible_invoice(item_id, user)
    values = {key: value for key, value in body.model_dump().items() if value is not None}
    merged = {**doc, **values}
    issues = [issue for issue in doc.get("issues", [])
              if "duplicate" in issue.lower() or "historical" in issue.lower()]
    calculation = round(float(merged.get("subtotal") or 0) + float(merged.get("tax") or 0)
                        - float(merged.get("discount") or 0), 2)
    if merged.get("total_amount") is None:
        issues.append("Total amount is required")
    elif abs(calculation - float(merged["total_amount"])) > 0.01:
        issues.append("Subtotal, tax, discount, and total do not reconcile")
    values.update({"issues": list(dict.fromkeys(issues)), "validation_status": "FAILED" if issues else "PASSED",
                   "status": "VALIDATED" if issues else "PENDING_APPROVAL"})
    collection("invoices").update_one({"_id": doc["_id"]}, {"$set": values})
    audit(user, "modified", "invoice", doc.get("invoice_number", item_id))
    return invoice_response(collection("invoices").find_one({"_id": doc["_id"]}))


@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...), department: Optional[str] = None,
                         user=Depends(require_permission('INVOICE_UPLOAD'))):
    if file.content_type not in {"application/pdf", "image/jpeg", "image/png"}:
        raise HTTPException(415, "Only PDF, JPG, and PNG invoices are supported")
    data = await file.read()
    if len(data) > 10 * 1024 * 1024: raise HTTPException(413, "Invoice must be smaller than 10 MB")
    text = extract_invoice_text(data, file.content_type)
    invoice_number = extract_field(text, ("invoice number", "invoice no", "invoice #"))
    vendor_name = extract_field(text, ("vendor", "supplier"), "Needs review")
    invoice_date = extract_field(text, ("invoice date", "date"), datetime.now().date().isoformat())
    due_date = extract_field(text, ("due date",), invoice_date)
    amount = extract_total(text)
    department = department_for(user, department)
    duplicate = next((invoice for invoice in visible_documents("invoices", user)
                      if invoice_number and invoice.get("invoice_number") == invoice_number), None)
    issues = ["Possible duplicate invoice detected"] if duplicate else []
    if not amount:
        issues.append("Total amount could not be extracted; enter it before approval")
    if not vendor_name or vendor_name == "Needs review":
        issues.append("Vendor could not be extracted; verify the vendor before approval")
    historical = [float(row.get("amount") or 0) for row in visible_documents("transactions", user)
                  if vendor_name and row.get("vendor_name") == vendor_name]
    if historical and amount > sum(historical) / len(historical) * 3:
        issues.append("Invoice amount is more than three times the historical vendor average")
    final_invoice_number = invoice_number or f"UPLOAD-{uuid.uuid4().hex[:6].upper()}"
    matched_vendor = next((item for item in visible_documents("vendors", user)
                           if vendor_name and str(item.get("vendor_name", "")).casefold() == vendor_name.casefold()), None)
    file_hash = hashlib.sha256(data).hexdigest()
    exact_duplicate = collection("invoices").find_one({"file_hash": file_hash})
    doc = {"_id": str(uuid.uuid4()), "invoice_number": final_invoice_number,
           "vendor_name": vendor_name, "vendor_id": matched_vendor.get("vendor_id") if matched_vendor else None,
           "invoice_date": invoice_date, "due_date": due_date,
           "subtotal": round(amount * .9, 2), "tax": round(amount * .1, 2), "discount": 0,
           "total_amount": amount, "currency": extract_field(text, ("currency",), "INR"),
           "line_items": [], "status": "PROCESSING", "processing_status": "EXTRACTED",
           "approval_status": "PENDING", "payment_status": "UNPAID",
           "file_hash": file_hash, "file_content": base64.b64encode(data).decode("ascii"),
           "file_content_type": file.content_type,
           "extraction_confidence": {"vendor_name": .98 if vendor_name != "Needs review" else .35,
                                     "invoice_number": .99 if invoice_number else .35,
                                     "total_amount": .97 if amount else .2,
                                     "invoice_date": .9 if invoice_date else .3,
                                     "due_date": .85 if due_date else .3},
           "confidence_score": .78 if not text else .91, "risk_level": "HIGH" if issues else "MEDIUM",
           "risk_score": min(100, 75 if issues else 45), "risk_reasons": issues or ["No extraction or duplicate indicators detected"],
           "issues": issues, "source_filename": file.filename,
           "department": department, "extraction_status": "EXTRACTED",
           "organization_id": user.get("organization_id"), "user_id": user["id"],
           "validation_status": "FAILED" if issues else "PASSED"}
    if exact_duplicate:
        doc["issues"].append("Exact duplicate upload detected")
    if amount and abs(doc["subtotal"] + doc["tax"] - doc["discount"] - amount) > 0.01:
        doc["issues"].append("Subtotal, tax, discount, and total do not reconcile")
        doc["validation_status"] = "FAILED"
    if doc["issues"]:
        doc["risk_level"] = "HIGH"
        doc["risk_score"] = min(100, max(int(doc.get("risk_score") or 0), 75))
        doc["risk_reasons"] = list(dict.fromkeys(doc.get("risk_reasons", []) + doc["issues"]))
    doc["status"] = "PENDING_APPROVAL" if not doc["issues"] else "VALIDATED"
    collection("invoices").insert_one(doc)
    audit(user, "uploaded", "invoice", doc["invoice_number"])
    return invoice_response(doc)


def _invoice_action(item_id, status, user):
    doc = _visible_invoice(item_id, user)
    if not can_manage_invoice(user):
        raise HTTPException(403, "Only Finance Managers or CFOs can approve or reject invoices")
    if status == "APPROVED" and doc.get("validation_status") == "FAILED":
        raise HTTPException(409, "Resolve invoice validation issues before approval")
    updates = {"status": status, "approval_status": status,
               "approved_by": user["id"] if status == "APPROVED" else None,
               "approved_at": datetime.now(timezone.utc).isoformat() if status == "APPROVED" else None}
    collection("invoices").update_one({"_id": doc["_id"]}, {"$set": updates})
    if status == "APPROVED":
        collection("notifications").insert_one({
            "_id": str(uuid.uuid4()), "type": "invoice_approved",
            "message": f"Invoice {doc.get('invoice_number')} approved and ready for payment",
            "invoice_id": doc["_id"], "department": doc.get("department"),
            "organization_id": doc.get("organization_id"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
    audit(user, status.lower(), "invoice", doc["invoice_number"])
    doc["status"] = status
    return invoice_response(doc)


@router.post("/{item_id}/payment")
def record_payment(item_id: str, body: PaymentRequest,
                   user=Depends(require_permission("INVOICE_PAYMENT"))):
    doc = _visible_invoice(item_id, user)
    if doc.get("approval_status") != "APPROVED":
        raise HTTPException(409, "Only approved invoices can be paid")
    existing_paid = sum(float(row.get("amount") or 0) for row in collection("transactions").find({"invoice_id": doc["_id"], "payment_type": "INVOICE_PAYMENT"}))
    outstanding = round(float(doc.get("total_amount") or 0) - existing_paid, 2)
    if body.amount > outstanding + .01:
        raise HTTPException(422, f"Payment exceeds outstanding amount of {outstanding:.2f}")
    transaction = {
        "_id": str(uuid.uuid4()), "transaction_id": f"PAY-{uuid.uuid4().hex[:8].upper()}",
        "invoice_id": doc["_id"], "date": datetime.now(timezone.utc).date().isoformat(),
        "amount": body.amount, "transaction_type": "EXPENSE", "category": "Invoice Payment",
        "description": f"Payment for invoice {doc.get('invoice_number')}",
        "vendor_id": doc.get("vendor_id"), "vendor_name": doc.get("vendor_name"),
        "payment_method": body.payment_method, "payment_reference": body.reference,
        "payment_type": "INVOICE_PAYMENT", "currency": doc.get("currency", "INR"),
        "status": "COMPLETED", "department": doc.get("department", "General"),
        "organization_id": doc.get("organization_id"), "user_id": user["id"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    collection("transactions").insert_one(transaction)
    sync_vendor_for_transaction(transaction)
    paid = round(existing_paid + body.amount, 2)
    payment_status = "PAID" if paid >= float(doc.get("total_amount") or 0) - .01 else "PARTIALLY_PAID"
    collection("invoices").update_one({"_id": doc["_id"]}, {"$set": {
        "payment_status": payment_status, "paid_amount": paid, "outstanding_amount": max(0, round(float(doc.get("total_amount") or 0) - paid, 2))
    }})
    audit(user, "payment_recorded", "invoice", doc["invoice_number"])
    return invoice_response(collection("invoices").find_one({"_id": doc["_id"]}))


@router.get("/{item_id}/document")
def invoice_document(item_id: str, user=Depends(require_permission("INVOICE_VIEW"))):
    doc = _visible_invoice(item_id, user)
    content = doc.get("file_content")
    if not content:
        raise HTTPException(404, "Invoice document is unavailable")
    return Response(content=base64.b64decode(content), media_type=doc.get("file_content_type", "application/pdf"),
                    headers={"Content-Disposition": f'inline; filename="{doc.get("source_filename", "invoice")}"'})


@router.get("/{item_id}/transactions")
def invoice_transactions(item_id: str, user=Depends(require_permission("INVOICE_VIEW"))):
    doc = _visible_invoice(item_id, user)
    return [serialize(row) for row in collection("transactions").find({"invoice_id": doc["_id"]})]


@router.get("/{item_id}/risk")
def invoice_risk(item_id: str, user=Depends(require_permission("INVOICE_VIEW"))):
    doc = _visible_invoice(item_id, user)
    return {
        "invoice_id": doc["_id"],
        "risk_score": doc.get("risk_score", 0),
        "risk_level": doc.get("risk_level", "LOW"),
        "flags": doc.get("risk_reasons", []),
        "explanation": "; ".join(doc.get("risk_reasons", [])) or "No risk indicators were detected.",
    }


@router.post("/{item_id}/approve")
def approve_invoice(item_id: str, user=Depends(require_permission('INVOICE_APPROVE'))):
    return _invoice_action(item_id, "APPROVED", user)


@router.post("/{item_id}/reject")
def reject_invoice(item_id: str, user=Depends(require_permission('INVOICE_REJECT'))):
    return _invoice_action(item_id, "REJECTED", user)
