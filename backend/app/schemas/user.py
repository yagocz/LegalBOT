from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import PlanType


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    avatar: Optional[str] = None
    plan: PlanType
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    avatar: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class SubscriptionResponse(BaseModel):
    id: UUID
    plan: PlanType
    status: str
    start_date: datetime
    end_date: Optional[datetime]
    
    class Config:
        from_attributes = True


class UsageResponse(BaseModel):
    queries_count: int
    queries_limit: int | str
    documents_count: int
    documents_limit: int | str
    month: str

