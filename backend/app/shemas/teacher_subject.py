from pydantic import BaseModel, Field

class TeacherSubjectBase(BaseModel):
    teacher_id: int  = Field(ge=1)
    subject_id: int = Field(ge=1)

class TeacherSubjectIn(BaseModel):
    FIO: str = Field(min_length = 1)
    subject: str = Field(min_length=1)
    #поля не могут быть пустыми

class SubjectName(BaseModel):
    name: str = Field(min_length=1)