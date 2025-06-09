import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class SubmissionsMark(BaseModel):
    id: int = Field(ge=1)
    mark: Optional[int] = Field(ge=1)
    comment: Optional[str] = Field(min_length=1, max_length=300)
    status: Optional[int] = Field(ge=0)

class SubmissionsID(BaseModel):
    id: int = Field(ge=1)
