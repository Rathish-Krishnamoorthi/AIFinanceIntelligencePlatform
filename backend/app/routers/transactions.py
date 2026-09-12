import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from ..core.security import get_current_user
from ..schemas.transaction import TransactionCreate
from ..services.common import audit, collection, serialize

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("")
def list_transactions(risk_level: Optional[str] = None, category: Optional[str] = None,
                      transaction_type: Optional[str] = None, limit: int = Query(100, le=500),
                      user=Depends(get_current_user)):
    rows = collection("transactions").find()
    if risk_level: rows = [x for x in rows if x.get("risk_level") == risk_level.upper()]
    if category: rows = [x for x in rows if x.get("category") == category]
    if transaction_type: rows = [x for x in rows if x.get("transaction_type") == transaction_type.upper()]
    return [serialize(x) for x in rows[:limit]]


@router.post("")
def create_transaction(body: TransactionCreate, user=Depends(get_current_user)):
    doc = body.model_dump()
    doc.update({"_id": str(uuid.uuid4()), "transaction_id": f"TX-{uuid.uuid4().hex[:8].upper()}",
                "created_at": datetime.now(timezone.utc).isoformat(), "risk_score": 15, "risk_level": "LOW"})
    collection("transactions").insert_one(doc)
    audit(user, "created", "transaction", doc["transaction_id"])
    return serialize(doc)


@router.get("/{item_id}")
def get_transaction(item_id: str, user=Depends(get_current_user)):
    found = collection("transactions").find_one({"transaction_id": item_id}) or collection("transactions").find_one({"_id": item_id})
    if not found: raise HTTPException(404, "Transaction not found")
    return serialize(found)


@router.put("/{item_id}")
def update_transaction(item_id: str, body: TransactionCreate, user=Depends(get_current_user)):
    found = collection("transactions").find_one({"transaction_id": item_id}) or collection("transactions").find_one({"_id": item_id})
    if not found: raise HTTPException(404, "Transaction not found")
    collection("transactions").update_one({"_id": found["_id"]}, {"$set": body.model_dump()})
    return serialize(collection("transactions").find_one({"_id": found["_id"]}))


@router.delete("/{item_id}")
def delete_transaction(item_id: str, user=Depends(get_current_user)):
    result = collection("transactions").delete_one({"transaction_id": item_id})
    return {"deleted": bool(result.deleted_count)}
