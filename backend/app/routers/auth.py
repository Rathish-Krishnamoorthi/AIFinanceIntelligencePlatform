import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..core.security import hash_password, verify_password, create_access_token, get_current_user
from ..schemas.user import RegisterRequest
from ..services.common import collection
from ..utils.validators import normalize_role

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
def register(body: RegisterRequest):
    if collection("users").find_one({"email": body.email}):
        raise HTTPException(409, "Email already registered")
    user = {"_id": str(uuid.uuid4()), "email": body.email, "name": body.name,
            "role": normalize_role(body.role), "password_hash": hash_password(body.password)}
    collection("users").insert_one(user)
    return {"access_token": create_access_token(user["_id"], user["role"]), "token_type": "bearer",
            "user": {k: user[k] for k in ("email", "name", "role")}}


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = collection("users").find_one({"email": form.username})
    if not user or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(401, "Incorrect email or password")
    return {"access_token": create_access_token(user["_id"], user["role"]), "token_type": "bearer",
            "user": {k: user[k] for k in ("email", "name", "role")}}


@router.get("/me")
def me(user=Depends(get_current_user)):
    found = collection("users").find_one({"_id": user["id"]})
    return {k: found[k] for k in ("email", "name", "role")} if found else user
