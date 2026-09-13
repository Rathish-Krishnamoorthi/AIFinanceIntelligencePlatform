from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..core.config import settings
from ..services.common import collection
from .permissions import Permission, UserRole, canonical_role, permissions_for_role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(subject: str, role: str) -> str:
    expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "role": role, "exp": expiry}, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        if not payload.get("sub"):
            raise ValueError()
        found = collection("users").find_one({"_id": payload["sub"]})
        if not found:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists")
        if found.get("is_active", True) is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive")
        role = found.get("role", UserRole.EMPLOYEE.value)
        if not canonical_role(role):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has an invalid role")
        return {"id": found["_id"], "email": found["email"], "name": found.get("name", ""),
                "role": role, "department": found.get("department"),
                "organization_id": found.get("organization_id"),
                "permissions": permissions_for_role(role),
                "canonical_role": canonical_role(role).value}
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token")

def require_roles(*roles):
    def dependency(user=Depends(get_current_user)):
        if roles and user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return dependency


def require_permission(permission: str | Permission):
    required = permission.value if isinstance(permission, Permission) else permission

    def dependency(user=Depends(get_current_user)):
        permissions = user.get("permissions", set())
        if "*" not in permissions and required not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You do not have permission to perform {required.lower().replace('_', ' ')}",
            )
        return user

    return dependency
