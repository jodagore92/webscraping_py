from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "admin"
    GENERAL = "general"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: Optional[str] = Field(None, alias="_id")
    hashed_password: str
    role: UserRole = UserRole.GENERAL
    is_active: bool = True

    model_config = {"populate_by_name": True}


class UserResponse(UserBase):
    id: str
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
