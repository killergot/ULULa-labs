from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID

MIN_LEN_PASS: int = 2

class UserBase(BaseModel):
    email: EmailStr
    role: Optional[int] = Field(ge=0, le=7)
    auth_provider: Optional[Literal['google', 'facebook', 'github','yandex']] = None
    provider_id: Optional[str] = None

    @field_validator('provider_id')
    @classmethod
    def check_provider(cls, v, values):
        if values.data.get('auth_provider') and not v:
            raise ValueError('provider_id required for OAuth')
        if v and not values.data.get('auth_provider'):
            raise ValueError('auth_provider required when provider_id is set')
        return v

class UserIn(UserBase):
    password: str =  Field(min_length=MIN_LEN_PASS,default=None)
    role: int = Field(ge=0, le=2)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdateIn(BaseModel):
    new_password: str = Field(min_length=MIN_LEN_PASS,default=None)
    old_password: str



class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        'from_attributes': True
    }

class TwoFactorIn(BaseModel):
    code: str = Field(max_length=6, min_length=6)
    session_token: str

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    type:str = 'Bearer'

    model_config = {
        'from_attributes': True
    }

class TwoFactorOut(BaseModel):
    session_token: str
    detail: str = "2FA required. Check your email."