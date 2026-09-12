from fastapi import APIRouter, Depends, HTTPException
from ..core.security import get_current_user
from ..services.common import collection, serialize

router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.get("")
def vendors(user=Depends(get_current_user)):
    return [serialize(x) for x in collection("vendors").find()]


@router.get("/{item_id}")
def vendor(item_id: str, user=Depends(get_current_user)):
    found = collection("vendors").find_one({"vendor_id": item_id})
    if not found: raise HTTPException(404, "Vendor not found")
    return serialize(found)


@router.get("/{item_id}/risk")
def vendor_risk(item_id: str, user=Depends(get_current_user)):
    found = collection("vendors").find_one({"vendor_id": item_id})
    return {"vendor_id": item_id, "risk_score": found.get("risk_score", 0) if found else 0,
            "factors": ["Invoice frequency", "Average amount deviation", "Payment history"]}
