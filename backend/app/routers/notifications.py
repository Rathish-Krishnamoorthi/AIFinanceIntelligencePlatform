from fastapi import APIRouter, Depends
from ..core.security import get_current_user, require_permission
from ..services.common import serialize, visible_documents

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def list_notifications(user=Depends(require_permission('NOTIFICATION_VIEW'))):
    return [serialize(x) for x in visible_documents("notifications", user)]
