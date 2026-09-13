from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=2)
    role: str = "ACCOUNTANT"
    department: str = "General"
    organization_id: str | None = None


class UserUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2)
    department: str | None = None
    job_title: str | None = None
    phone: str | None = None
    profile_image: str | None = None


class ProfileUpdateRequest(UserUpdateRequest):
    pass


class RoleUpdateRequest(BaseModel):
    role: str


class StatusUpdateRequest(BaseModel):
    is_active: bool
