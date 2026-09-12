from datetime import datetime, timezone
import uuid
from ..core.database import store


def collection(name):
    return store.collection(name)


def serialize(document):
    if not document:
        return None
    result = dict(document)
    result.pop("_id", None)
    return result


def audit(user, action, entity_type, entity_id, reason=""):
    collection("audit_logs").insert_one({
        "_id": str(uuid.uuid4()), "user_id": user["id"], "action": action,
        "entity_type": entity_type, "entity_id": entity_id,
        "timestamp": datetime.now(timezone.utc).isoformat(), "reason": reason,
    })
