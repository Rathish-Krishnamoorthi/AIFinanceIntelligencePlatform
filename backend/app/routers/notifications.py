from fastapi import APIRouter, Depends
from ..core.security import get_current_user
from ..services.common import collection, serialize

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def list_notifications(user=Depends(get_current_user)):
    return [serialize(x) for x in collection("notifications").find()]
