import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
import pandas as pd
from ..core.security import get_current_user, require_permission
from ..schemas.transaction import TransactionCreate
from ..services.common import audit, collection, department_for, refresh_vendor, serialize, sync_vendor_for_transaction, visible_documents
from ..services.anomaly_service import transaction_risk

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("")
def list_transactions(risk_level: Optional[str] = None, category: Optional[str] = None,
                      transaction_type: Optional[str] = None, search: Optional[str] = None,
                      sort_by: str = Query("date"), sort_order: str = Query("desc", pattern="^(asc|desc)$"),
                      page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=500),
                      user=Depends(require_permission('TRANSACTION_VIEW'))):
    rows = visible_documents("transactions", user)
    if risk_level: rows = [x for x in rows if x.get("risk_level") == risk_level.upper()]
    if category: rows = [x for x in rows if x.get("category") == category]
    if transaction_type: rows = [x for x in rows if x.get("transaction_type") == transaction_type.upper()]
    if search:
        needle = search.casefold()
        rows = [x for x in rows if needle in " ".join(str(x.get(key, "")) for key in
                ("transaction_id", "category", "description", "vendor_id", "payment_method")).casefold()]
    rows.sort(key=lambda item: str(item.get(sort_by, "")), reverse=sort_order == "desc")
    total = len(rows)
    start = (page - 1) * page_size
    return {"items": [serialize(x) for x in rows[start:start + page_size]],
            "total": total, "page": page, "page_size": page_size}


@router.post("")
def create_transaction(body: TransactionCreate, user=Depends(require_permission('TRANSACTION_CREATE'))):
    doc = body.model_dump()
    doc["department"] = department_for(user, doc.get("department"))
    doc["organization_id"] = user.get("organization_id")
    doc["user_id"] = user["id"]
    doc.update({"_id": str(uuid.uuid4()), "transaction_id": f"TX-{uuid.uuid4().hex[:8].upper()}",
                "created_at": datetime.now(timezone.utc).isoformat()})
    score, level, reasons = transaction_risk(doc, user)
    doc.update({"risk_score": score, "risk_level": level, "risk_reasons": reasons})
    collection("transactions").insert_one(doc)
    sync_vendor_for_transaction(doc)
    collection("transactions").update_one({"_id": doc["_id"]}, {"$set": {"vendor_id": doc.get("vendor_id")}})
    refresh_vendor(doc.get("vendor_id"), doc)
    audit(user, "created", "transaction", doc["transaction_id"])
    return serialize(doc)


@router.get("/{item_id}")
def get_transaction(item_id: str, user=Depends(require_permission('TRANSACTION_VIEW'))):
    found = collection("transactions").find_one({"transaction_id": item_id}) or collection("transactions").find_one({"_id": item_id})
    if not found or found not in visible_documents("transactions", user): raise HTTPException(404, "Transaction not found")
    return serialize(found)


@router.put("/{item_id}")
def update_transaction(item_id: str, body: TransactionCreate, user=Depends(require_permission('TRANSACTION_UPDATE'))):
    found = collection("transactions").find_one({"transaction_id": item_id}) or collection("transactions").find_one({"_id": item_id})
    if not found or found not in visible_documents("transactions", user): raise HTTPException(404, "Transaction not found")
    values = body.model_dump()
    values["department"] = department_for(user, values.get("department"))
    values["_id"] = found["_id"]
    score, level, reasons = transaction_risk(values, user)
    values.update({"risk_score": score, "risk_level": level, "risk_reasons": reasons})
    collection("transactions").update_one({"_id": found["_id"]}, {"$set": values})
    sync_vendor_for_transaction(values)
    if found.get("vendor_id") and found.get("vendor_id") != values.get("vendor_id"):
        refresh_vendor(found["vendor_id"])
    audit(user, "updated", "transaction", found["transaction_id"])
    return serialize(collection("transactions").find_one({"_id": found["_id"]}))


@router.delete("/{item_id}")
def delete_transaction(item_id: str, user=Depends(require_permission('TRANSACTION_DELETE'))):
    found = collection("transactions").find_one({"transaction_id": item_id}) or collection("transactions").find_one({"_id": item_id})
    if not found or found not in visible_documents("transactions", user):
        raise HTTPException(404, "Transaction not found")
    result = collection("transactions").delete_one({"_id": found["_id"]})
    if result.deleted_count:
        refresh_vendor(found.get("vendor_id"))
        audit(user, "deleted", "transaction", item_id)
    return {"deleted": bool(result.deleted_count)}


@router.post("/import")
async def import_transactions(file: UploadFile = File(...), department: Optional[str] = None,
                              user=Depends(require_permission('TRANSACTION_CREATE'))):
    suffix = (file.filename or "").lower().rsplit(".", 1)[-1]
    if suffix not in {"csv", "xlsx", "xls"}:
        raise HTTPException(415, "Upload a CSV or Excel file")
    data = await file.read()
    if len(data) > 25 * 1024 * 1024:
        raise HTTPException(413, "File must be smaller than 25 MB")
    try:
        from io import BytesIO
        frame = pd.read_csv(BytesIO(data)) if suffix == "csv" else pd.read_excel(BytesIO(data))
    except Exception as exc:
        raise HTTPException(422, f"Could not read the file: {exc}") from exc
    aliases = {
        "transaction_id": "transaction_id", "date": "date", "amount": "amount",
        "transaction_type": "transaction_type", "type": "transaction_type",
        "category": "category", "description": "description", "vendor_id": "vendor_id",
        "vendor_name": "vendor_name",
        "account": "account", "payment_method": "payment_method", "currency": "currency",
        "status": "status", "department": "department",
    }
    frame.columns = [str(column).strip().lower().replace(" ", "_") for column in frame.columns]
    frame = frame.rename(columns={column: aliases[column] for column in frame.columns if column in aliases})
    required = {"date", "amount", "transaction_type", "category"}
    missing = required - set(frame.columns)
    if missing:
        raise HTTPException(422, f"Missing required columns: {', '.join(sorted(missing))}")
    imported = []
    for row in frame.where(pd.notna(frame), None).to_dict("records"):
        try:
            amount = float(row["amount"])
            if amount <= 0:
                raise ValueError("amount must be greater than zero")
        except (TypeError, ValueError) as exc:
            raise HTTPException(422, f"Invalid amount in imported row: {exc}") from exc
        doc = {
            "_id": str(uuid.uuid4()),
            "transaction_id": str(row.get("transaction_id") or f"TX-{uuid.uuid4().hex[:8].upper()}"),
            "date": str(row["date"]), "amount": amount,
            "transaction_type": str(row["transaction_type"]).upper(),
            "category": str(row["category"]), "description": str(row.get("description") or ""),
            "vendor_id": row.get("vendor_id"), "account": str(row.get("account") or "Operating"),
            "payment_method": str(row.get("payment_method") or "Bank transfer"),
            "currency": str(row.get("currency") or "INR"), "status": str(row.get("status") or "COMPLETED"),
            "department": department_for(user, str(row.get("department") or department or "")),
            "user_id": user["id"], "organization_id": user.get("organization_id"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        score, level, reasons = transaction_risk(doc, user)
        doc.update({"risk_score": score, "risk_level": level, "risk_reasons": reasons})
        collection("transactions").insert_one(doc)
        sync_vendor_for_transaction(doc)
        collection("transactions").update_one({"_id": doc["_id"]}, {"$set": {"vendor_id": doc.get("vendor_id")}})
        refresh_vendor(doc.get("vendor_id"), doc)
        imported.append(serialize(doc))
    audit(user, "imported", "transactions", file.filename or "upload")
    return {"imported": len(imported), "transactions": imported}
