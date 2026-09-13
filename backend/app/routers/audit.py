from fastapi import APIRouter, Depends
from ..core.security import get_current_user, require_permission
from ..services.common import collection, serialize

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("")
def list_audit_logs(user=Depends(require_permission('AUDIT_VIEW'))):
    return [serialize(x) for x in collection("audit_logs").find()]
