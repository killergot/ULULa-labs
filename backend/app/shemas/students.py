import re
from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException, status

from pydantic import BaseModel, EmailStr, field_validator, Field

from app.database.models.students import Student


class StudentID(BaseModel):
    student_id: int = Field(ge = 1)


class StudentBase(BaseModel):
    student_id: int = Field(ge = 1)
    group_id: int = Field(ge=1)


class StudentIn(BaseModel): #Используется при регистрации студента по номеру группы, а не по id
    group_number: str = Field(min_length=1)
    full_name: str

class StudentUpdateIn(BaseModel): #Используется при регистрации студента по номеру группы, а не по id
    group_number: Optional[str] = Field(min_length=1,default=None)
    full_name: Optional[str] = Field(min_length=1,default=None)
    email: Optional[EmailStr] = None
    telegram: Optional[str] = None
    avatar_url: Optional[str] = None
    nickname: Optional[str] = None

    @field_validator('avatar_url')
    def name_must_contain_space(cls, v):
        pattern = r"^https?://[^/]+(/[^?#]*)?(\.jpg|\.jpeg|\.png|\.gif|\.webp)(\?.*)?$"
        if v and not re.match(pattern, v, re.I):
            print(v)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='only https://vk.com/')
        if v and ('javascript' in v or 'data' in v):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='"javascript" or "data" are not allowed')
        return v



class Achievement(BaseModel):
    name: str
    description: str
    amount: int = Field(ge=1)

    model_config = {
        'from_attributes': True
    }

class StudentOut(StudentID, StudentIn):
    email: Optional[EmailStr] = None
    achievements: Optional[list] = Field(default_factory=list) #Optional[List[Achievement]] = Field(default_factory=list) # Почему тут ошибка?
    telegram: Optional[str] = None
    avatar_url: Optional[str] = None
    nickname: Optional[str] = None

    model_config = {
        'from_attributes': True
    }