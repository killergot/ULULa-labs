import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class AssignmentsIn(BaseModel):
    group_id: int = Field(ge=1)
    lab_id: int = Field(ge=1)
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
    deadline_at: datetime.datetime = Field(default=datetime.timedelta(days=7)+datetime.datetime.now())
    status: int = Field(ge=0)

@field_validator('deadline_at')
@classmethod
def validate_deadline_at(cls, value: datetime.datetime) -> datetime.datetime:
        min_date = datetime.datetime.now()+datetime.timedelta(days=1) # Минимальная дата (сегодня)
        if value < min_date:
            raise ValueError(f"Дата не может быть раньше {min_date}")
        return value

class AssignmentID(BaseModel):
    id: int = Field(ge = 1)


