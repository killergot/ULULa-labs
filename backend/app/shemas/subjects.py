from pydantic import BaseModel, Field


class SubjectName(BaseModel):
    name: str = Field(min_length=1)