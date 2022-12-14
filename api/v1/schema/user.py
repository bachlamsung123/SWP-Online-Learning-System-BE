from datetime import date

from pydantic import BaseModel, EmailStr, validator

from ..database.user import UserRole
from .base import CommonAttrs


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str
    gender: bool
    dob: date
    phone: str
    address: str
    bio: str
    avatar: str | None


class UserUpdate(BaseModel):
    full_name: str | None
    gender: bool | None
    dob: date | None
    phone: str | None
    address: str | None
    bio: str | None
    avatar: str | None


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserChangeRole(BaseModel):
    role: str

    @validator("role")
    def validate_role(cls, role):
        if role not in UserRole.ALL:
            raise ValueError(f"Role must be one of {UserRole.ALL}")
        return role


class UserResetPasswordRequest(BaseModel):
    email: EmailStr


class UserResetPassword(BaseModel):
    password: str


class User(CommonAttrs):
    username: str
    email: EmailStr
    full_name: str
    gender: bool
    dob: date
    phone: str
    address: str
    bio: str
    role: str
    avatar: str | None
