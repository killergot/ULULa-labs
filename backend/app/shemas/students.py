from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, Field

class StudentBase(BaseModel):
    student_id: int = Field(ge = 1)
    group_id: int = Field(ge=1)


class StudentIn(BaseModel): #Используется при регистрации студента по номеру группы, а не по id
    group_number: str = Field(min_length=1)
    full_name: str


class Achievement(BaseModel):
    name: str
    description: str
    amount: int = Field(ge=1)

class StudentOut(StudentIn):
    student_id: int = Field(ge = 1)
    email: Optional[EmailStr]
    achievements: Optional[list[Achievement]]
    telegram: Optional[str]
    avatar_url: Optional[str]
    nickname: Optional[str]

    model_config = {
        'from_attributes': True
    }


class StudentID(BaseModel):
    student_id: int = Field(ge = 1)

