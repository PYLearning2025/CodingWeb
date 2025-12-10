from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from map import UserRole, UserStatus

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: Optional[str] = None
    role: UserRole = Field(default=UserRole.USER)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    avatar: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserCreate(UserBase):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserUpdate(UserBase):
    pass

class UserLogin(BaseModel):
    name: str
    password: str

class LoginResponse(BaseModel):
    token: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)