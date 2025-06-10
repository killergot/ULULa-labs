from typing import Optional

from pydantic import BaseModel,Field


class LabWorkIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1, max_length=500)#поля не могут быть пустыми
    subject_name: str = Field(min_length=1, max_length=200)
    file_id: Optional[int] = Field(ge=1, default=None)

class LabWorkID(BaseModel):
    id: int = Field(ge=1)