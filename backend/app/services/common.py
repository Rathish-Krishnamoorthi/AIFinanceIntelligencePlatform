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
        "role": user.get("role"), "module": entity_type,
        "timestamp": datetime.now(timezone.utc).isoformat(), "reason": reason,
        "result": "success",
    })


def can_manage_all(user):
    return user.get("canonical_role") in {"SYSTEM_ADMIN", "CFO", "FINANCE_MANAGER"} or \
        user.get("role") in {"ADMIN", "FINANCE_MANAGER", "AUDITOR"}


def visible_documents(name, user):
    rows = collection(name).find()
    organization_id = user.get("organization_id")
    if organization_id:
        rows = [row for row in rows if not row.get("organization_id") or row.get("organization_id") == organization_id]
    if user.get("canonical_role") == "EMPLOYEE" or user.get("role") == "ACCOUNTANT":
        rows = [row for row in rows if row.get("user_id") == user.get("id")]
    if can_manage_all(user) or not user.get("department"):
        return rows
    return [row for row in rows if not row.get("department") or row.get("department") == user["department"]]


def department_for(user, requested=None):
    if requested and can_manage_all(user):
        return requested.strip()
    return user.get("department") or "General"


def sync_vendor_for_transaction(transaction):
    """Create or refresh the vendor aggregate associated with a transaction."""
    vendor_id = transaction.get("vendor_id")
    vendor_name = (transaction.get("vendor_name") or "").strip()
    if not vendor_id and not vendor_name:
        return None

    vendors = collection("vendors")
    vendor = vendors.find_one({"vendor_id": vendor_id}) if vendor_id else None
    if not vendor and vendor_name:
        vendor = next((item for item in vendors.find()
                       if str(item.get("vendor_name", "")).casefold() == vendor_name.casefold()), None)
    if not vendor:
        vendor_id = vendor_id or f"VEN-{uuid.uuid4().hex[:8].upper()}"
        vendor = {
            "_id": str(uuid.uuid4()), "vendor_id": vendor_id, "vendor_name": vendor_name or vendor_id,
            "department": transaction.get("department", "General"),
            "organization_id": transaction.get("organization_id"),
        }
        vendors.insert_one(vendor)
    else:
        vendor_id = vendor.get("vendor_id")

    transaction["vendor_id"] = vendor_id
    refresh_vendor(vendor_id, transaction)
    return vendor_id


def refresh_vendor(vendor_id, context=None):
    if not vendor_id:
        return
    vendors = collection("vendors")
    vendor = vendors.find_one({"vendor_id": vendor_id})
    if not vendor:
        return
    related = [item for item in collection("transactions").find({"vendor_id": vendor_id})]
    expenses = [item for item in related if item.get("transaction_type") == "EXPENSE"]
    total_spend = sum(float(item.get("amount") or 0) for item in expenses)
    risk_scores = [float(item.get("risk_score") or 0) for item in related]
    updates = {
        "vendor_name": (context or {}).get("vendor_name") or vendor.get("vendor_name", vendor_id),
        "total_spend": round(total_spend, 2),
        "transaction_count": len(related),
        "last_transaction_date": max((str(item.get("date", "")) for item in related), default=None),
        "risk_score": round(sum(risk_scores) / len(risk_scores)) if risk_scores else 0,
        "department": (context or {}).get("department") or vendor.get("department", "General"),
        "organization_id": (context or {}).get("organization_id") or vendor.get("organization_id"),
    }
    vendors.update_one({"_id": vendor["_id"]}, {"$set": updates})
