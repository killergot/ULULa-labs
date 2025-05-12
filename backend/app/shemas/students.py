from typing import Optional, List

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



class Achievement(BaseModel):
    name: str
    description: str
    amount: int = Field(ge=1)

    model_config = {
        'from_attributes': True
    }

class StudentOut(StudentID, StudentIn):
    student_id: int = Field(ge = 1)
    email: Optional[EmailStr] = None
    achievements: Optional[list] = Field(default_factory=list) #Optional[List[Achievement]] = Field(default_factory=list) # Почему тут ошибка?
    telegram: Optional[str] = None
    avatar_url: Optional[str] = None
    nickname: Optional[str] = None

    model_config = {
        'from_attributes': True
    }