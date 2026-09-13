from fastapi import APIRouter, Depends, HTTPException
from ..core.security import get_current_user, require_permission
from ..services.common import collection, serialize, visible_documents

router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.get("")
def vendors(user=Depends(require_permission('VENDOR_VIEW'))):
    return [serialize(x) for x in visible_documents("vendors", user)]


@router.get("/{item_id}")
def vendor(item_id: str, user=Depends(require_permission('VENDOR_VIEW'))):
    found = next((item for item in visible_documents("vendors", user)
                  if item.get("vendor_id") == item_id), None)
    if not found: raise HTTPException(404, "Vendor not found")
    return serialize(found)


@router.get("/{item_id}/risk")
def vendor_risk(item_id: str, user=Depends(require_permission('VENDOR_VIEW'))):
    found = next((item for item in visible_documents("vendors", user)
                  if item.get("vendor_id") == item_id), None)
    return {"vendor_id": item_id, "risk_score": found.get("risk_score", 0) if found else 0,
            "factors": ["Invoice frequency", "Average amount deviation", "Payment history"]}


@router.get("/{item_id}/invoices")
def vendor_invoices(item_id: str, user=Depends(require_permission('VENDOR_VIEW'))):
    vendor = next((item for item in visible_documents("vendors", user)
                   if item.get("vendor_id") == item_id), None)
    if not vendor:
        raise HTTPException(404, "Vendor not found")
    return [serialize(item) for item in visible_documents("invoices", user)
            if item.get("vendor_id") == item_id]


@router.get("/{item_id}/transactions")
def vendor_transactions(item_id: str, user=Depends(require_permission('VENDOR_VIEW'))):
    vendor = next((item for item in visible_documents("vendors", user)
                   if item.get("vendor_id") == item_id), None)
    if not vendor:
        raise HTTPException(404, "Vendor not found")
    return [serialize(item) for item in visible_documents("transactions", user)
            if item.get("vendor_id") == item_id]
