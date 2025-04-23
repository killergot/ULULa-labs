from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID

MIN_LEN_PASS: int = 2

class StudentBase(BaseModel):
    student_id: int
    group_id: int
    #поля не могут быть пустыми

    @field_validator('student_id')
    @classmethod
    def validate_user_id(cls, v):
        if v is None or v == 0:
            raise ValueError('Student ID cannot be empty or zero')
        return v

    @field_validator('group_id')
    @classmethod
    def validate_group_id(cls, v):
        if v is None or v == 0:
            raise ValueError('Group ID cannot be empty or zero')
        return v

class StudentIn(BaseModel): #Используется при регистрации студента по номеру группы, а не по id
    student_id: int
    group_number: str
    # поля не могут быть пустыми

    @field_validator('student_id' )
    def check_id_not_empty(cls, v):
        if v is None or v == 0:  # Проверка на None и 0
            raise ValueError('ID cannot be empty or zero')
        return v
    @field_validator('group_number')
    def check_num_not_empty(cls, v):
        if v is None:  # Проверка на None и 0
            raise ValueError('Number cannot be empty')
        return v

'''
class UserIn(UserBase):
    password: str =  Field(min_length=MIN_LEN_PASS,default=None)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdateIn(BaseModel):
    id: int
    password: str



class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        'from_attributes': True
    }

class TokenOut(BaseModel):
    access_token: str
    expires_at: datetime

    model_config = {
        'from_attributes': True
    }

class TwoFactorOut(BaseModel):
    session_token: str
    detail: str = "2FA required. Check your email."\
'''