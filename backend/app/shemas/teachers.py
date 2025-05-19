from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, Field

class FIO(BaseModel):
    FIO: str = Field(min_length=1)

class WeekNumber(BaseModel):
    week_number: int = Field(ge=1, le=4)
    #поля не могут быть пустыми

class TeacherOut(FIO):
    id: int
    email: EmailStr
    avatar: Optional[str] = None
    telegram: Optional[str] = None
    nickname: Optional[str] = None
