import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..core.security import hash_password, verify_password, create_access_token, get_current_user
from ..core.permissions import permissions_for_role
from ..schemas.user import ProfileUpdateRequest, RegisterRequest
from ..services.common import collection
from ..utils.validators import normalize_role

router = APIRouter(prefix="/auth", tags=["authentication"])


def _profile(found, user):
    role = found.get("role", user.get("role"))
    return {
        "id": found.get("_id"),
        "email": found.get("email"),
        "name": found.get("name", ""),
        "role": role,
        "canonical_role": user.get("canonical_role"),
        "department": found.get("department"),
        "organization_id": found.get("organization_id"),
        "job_title": found.get("job_title", ""),
        "phone": found.get("phone", ""),
        "profile_image": found.get("profile_image"),
        "is_active": found.get("is_active", True),
        "created_at": found.get("created_at"),
        "permissions": sorted(permissions_for_role(role)),
    }


@router.post("/register")
def register(body: RegisterRequest):
    email = str(body.email).strip().lower()
    if collection("users").find_one({"email": email}):
        raise HTTPException(409, "Email already registered")
    # Public registration can never provision a privileged role.
    role = "EMPLOYEE"
    user = {"_id": str(uuid.uuid4()), "email": email, "name": body.name.strip(),
            "role": role, "department": body.department.strip() or "General",
            "organization_id": body.organization_id, "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "password_hash": hash_password(body.password)}
    collection("users").insert_one(user)
    return {"access_token": create_access_token(user["_id"], user["role"]), "token_type": "bearer",
            "user": {**{k: user[k] for k in ("email", "name", "role", "department")},
                     "permissions": sorted(permissions_for_role(role))}}


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    email = form.username.strip().lower()
    user = collection("users").find_one({"email": email})
    if not user or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(401, "Incorrect email or password")
    return {"access_token": create_access_token(user["_id"], user["role"]), "token_type": "bearer",
            "user": {**{k: user[k] for k in ("email", "name", "role", "department")},
                     "permissions": sorted(permissions_for_role(user["role"]))}}


@router.get("/me")
def me(user=Depends(get_current_user)):
    found = collection("users").find_one({"_id": user["id"]})
    return _profile(found, user) if found else user


@router.get("/profile")
def profile(user=Depends(get_current_user)):
    found = collection("users").find_one({"_id": user["id"]})
    if not found:
        raise HTTPException(404, "User profile not found")
    return _profile(found, user)


@router.put("/profile")
def update_profile(body: ProfileUpdateRequest, user=Depends(get_current_user)):
    update = {key: value for key, value in body.model_dump().items() if value is not None}
    if body.profile_image and len(body.profile_image) > 3_000_000:
        raise HTTPException(413, "Profile image is too large")
    if not update:
        raise HTTPException(400, "No profile fields supplied")
    result = collection("users").update_one({"_id": user["id"]}, {"$set": update})
    if not getattr(result, "matched_count", getattr(result, "modified_count", 0)):
        raise HTTPException(404, "User profile not found")
    found = collection("users").find_one({"_id": user["id"]})
    return _profile(found, user)
