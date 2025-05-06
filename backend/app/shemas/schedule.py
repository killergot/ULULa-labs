from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, Literal
from datetime import datetime


class ScheduleBase(BaseModel):
    group_id: int = Field(ge=1)
    week_number: int = Field(ge=1, le=4 )
    monday: list
    tuesday: list
    wednesday: list
    thursday: list
    friday: list
    saturday: list
    sunday: list

class ScheduleIn(BaseModel):
    group_number: str = Field(min_length=1)
    week_number: int = Field(ge=1, le=4 )
    monday: list
    tuesday: list
    wednesday: list
    thursday: list
    friday: list
    saturday: list
    sunday: list
    #поля не могут быть пустыми

class ScheduleGetIn(BaseModel):
    group_id: int = Field(ge=1)
    week_number: int = Field(ge=1, le=4)