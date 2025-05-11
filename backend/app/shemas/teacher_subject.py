from pydantic import BaseModel, Field


class TeacherSubjectIn(BaseModel):
    FIO: str = Field(min_length = 1)
    subject: str = Field(min_length=1)
    #поля не могут быть пустыми

