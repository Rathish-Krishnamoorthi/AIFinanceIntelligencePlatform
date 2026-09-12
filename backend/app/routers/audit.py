from fastapi import APIRouter, Depends
from ..core.security import get_current_user
from ..services.common import collection, serialize

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("")
def list_audit_logs(user=Depends(get_current_user)):
    return [serialize(x) for x in collection("audit_logs").find()]
