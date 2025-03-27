from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID, uuid4

class UserBase(BaseModel):
    email: EmailStr
    role: Optional[str] = 'user'
    auth_provider: Optional[Literal['google', 'facebook', 'github','yandex']] = None
    provider_id: Optional[str] = None

    @field_validator('provider_id')
    def check_provider(cls, v, values):
        if values.data.get('auth_provider') and not v:
            raise ValueError('provider_id required for OAuth')
        if v and not values.data.get('auth_provider'):
            raise ValueError('auth_provider required when provider_id is set')
        return v


class UserCreate(UserBase):
    password: Optional[str] = None

    @field_validator('password')
    def check_password(cls, v, values):
        if not v and not values.data.get('auth_provider'):
            raise ValueError('Password is required for non-OAuth registration')
        return v


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # Вместо orm_mode в Pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str

class TwoFactorRequest(BaseModel):
    session_token: str
    detail: str = "2FA required. Check your email."

class TokenData(BaseModel):
    user_id: Optional[str] = None