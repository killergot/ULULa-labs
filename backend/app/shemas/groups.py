from pydantic import BaseModel, EmailStr, field_validator, Field


class GroupBase(BaseModel):
    group_id: int = Field(ge = 1)
    group_number: str = Field(min_length=1)
    #поля не могут быть пустыми


class GroupNumber(BaseModel): #Используется при регистрации студента по номеру группы, а не по id
    group_number: str = Field(min_length=1)
    # поля не могут быть пустыми

class GroupID(BaseModel): #Используется при регистрации студента по номеру группы, а не по id
    group_id: int = Field(ge = 1)