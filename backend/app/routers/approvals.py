from fastapi import APIRouter, Depends
from ..core.security import get_current_user
from ..services.common import collection, serialize

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.get("")
def pending_approvals(user=Depends(get_current_user)):
    return [serialize(x) for x in collection("invoices").find({"status": "PENDING_APPROVAL"})]
