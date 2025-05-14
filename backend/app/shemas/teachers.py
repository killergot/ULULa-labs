from pydantic import BaseModel, EmailStr, field_validator, Field

class FIO(BaseModel):
    FIO: str = Field(min_length=1)

class WeekNumber(BaseModel):
    week_number: int = Field(ge=1, le=4)
    #поля не могут быть пустыми

'''
class StudentBase(BaseModel):
    student_id: int = Field(ge = 1)
    group_id: int = Field(ge=1)
    #поля не могут быть пустыми


class StudentIn(BaseModel): #Используется при регистрации студента по номеру группы, а не по id
    group_number: str = Field(min_length=1)
    # поля не могут быть пустыми


class StudentID(BaseModel): 
    student_id: int = Field(ge = 1)
    # поля не могут быть пустыми
'''