from pydantic import BaseModel, Field


class GroupSubjectIn(BaseModel):
    group_number: str = Field(min_length = 1)
    subject: str = Field(min_length=1)
    #поля не могут быть пустыми

