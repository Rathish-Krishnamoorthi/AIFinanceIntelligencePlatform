import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from ..core.security import hash_password, require_permission, require_roles
from ..schemas.user import RegisterRequest, RoleUpdateRequest, StatusUpdateRequest, UserUpdateRequest
from ..core.permissions import UserRole, canonical_role
from ..services.common import audit, collection, serialize
from ..utils.validators import normalize_role

router = APIRouter(prefix="/admin", tags=["administration"])


def _is_system_admin(record):
    return canonical_role(record.get("role")) == UserRole.SYSTEM_ADMIN


def _active_system_admin_count():
    return collection("users").count_documents({
        "role": {"$in": [UserRole.SYSTEM_ADMIN.value, UserRole.ADMIN.value]},
        "is_active": {"$ne": False},
    })


@router.get("/departments")
def departments(user=Depends(require_permission("USER_VIEW"))):
    names = {row.get("department") for row in collection("users").find() if row.get("department")}
    names.update(row.get("department") for row in collection("transactions").find() if row.get("department"))
    names.update(row.get("department") for row in collection("invoices").find() if row.get("department"))
    return sorted(name for name in names if name)


@router.get("/users")
def users(user=Depends(require_permission('USER_VIEW'))):
    return [{**{"_id": row.get("_id")}, **{key: row.get(key) for key in ("email", "name", "role", "department", "is_active")}}
            for row in collection("users").find()]


@router.post("/users")
def create_user(body: RegisterRequest, user=Depends(require_permission('USER_CREATE'))):
    email = str(body.email).strip().lower()
    if collection("users").find_one({"email": email}):
        raise HTTPException(409, "Email already registered")
    role = normalize_role(body.role)
    record = {"_id": str(uuid.uuid4()), "email": email, "name": body.name.strip(),
              "role": role, "department": body.department.strip() or "General",
              "organization_id": body.organization_id or user.get("organization_id"),
              "is_active": True,
              "created_at": datetime.now(timezone.utc).isoformat(),
              "password_hash": hash_password(body.password)}
    collection("users").insert_one(record)
    audit(user, "created", "user", record["_id"])
    return {key: record[key] for key in ("email", "name", "role", "department")}


@router.get("/users/{user_id}")
def get_user(user_id: str, user=Depends(require_permission("USER_VIEW"))):
    found = collection("users").find_one({"_id": user_id})
    if not found:
        raise HTTPException(404, "User not found")
    return {key: found.get(key) for key in ("_id", "email", "name", "role", "department", "is_active")}


@router.put("/users/{user_id}")
def update_user(user_id: str, body: UserUpdateRequest, user=Depends(require_permission("USER_UPDATE"))):
    update = {key: value for key, value in body.model_dump().items() if value is not None}
    if not update:
        raise HTTPException(400, "No user fields supplied")
    result = collection("users").update_one({"_id": user_id}, {"$set": update})
    audit(user, "updated", "user", user_id)
    if not result.matched_count:
        raise HTTPException(404, "User not found")
    return get_user(user_id, user)


@router.patch("/users/{user_id}/role")
def update_role(user_id: str, body: RoleUpdateRequest, user=Depends(require_permission("USER_ROLE_UPDATE"))):
    if body.role not in {role.value for role in UserRole}:
        raise HTTPException(422, "Invalid role")
    target = collection("users").find_one({"_id": user_id})
    if not target:
        raise HTTPException(404, "User not found")
    if _is_system_admin(target) and canonical_role(body.role) != UserRole.SYSTEM_ADMIN:
        if _active_system_admin_count() <= 1:
            raise HTTPException(409, "Cannot remove the last active administrator")
    collection("users").update_one({"_id": user_id}, {"$set": {"role": body.role}})
    audit(user, "role_changed", "user", user_id)
    return get_user(user_id, user)


@router.patch("/users/{user_id}/status")
def update_status(user_id: str, body: StatusUpdateRequest, user=Depends(require_permission("USER_UPDATE"))):
    target = collection("users").find_one({"_id": user_id})
    if not target:
        raise HTTPException(404, "User not found")
    if _is_system_admin(target) and not body.is_active:
        if _active_system_admin_count() <= 1:
            raise HTTPException(409, "Cannot deactivate the last active administrator")
    collection("users").update_one({"_id": user_id}, {"$set": {"is_active": body.is_active}})
    audit(user, "status_changed", "user", user_id)
    return get_user(user_id, user)


@router.delete("/users/{user_id}")
def delete_user(user_id: str, user=Depends(require_permission("USER_DELETE"))):
    target = collection("users").find_one({"_id": user_id})
    if not target:
        raise HTTPException(404, "User not found")
    if _is_system_admin(target) and _active_system_admin_count() <= 1:
        raise HTTPException(409, "Cannot delete the last active administrator")
    collection("users").delete_one({"_id": user_id})
    audit(user, "deleted", "user", user_id)
    return {"deleted": user_id}
