from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, Field
from fastapi import Query

class GroupBase(BaseModel):
    group_id: int = Field(ge = 1)
    group_number: str = Field(min_length=1)
    #поля не могут быть пустыми


class GroupNumber(BaseModel): #Используется при регистрации студента по номеру группы, а не по id
    group_number: str = Field(min_length=1)

    model_config = {
        'from_attributes': True
    }

class GroupID(BaseModel): #Используется при регистрации студента по номеру группы, а не по id
    group_id: int = Field(ge = 1)

class FileBase(BaseModel):
    group_number: str
    subject: str

class FileIn(FileBase):
    filename: str = Field(min_length=1)
    filesize: int = Field(ge=1)

class FilesFilteredIn(BaseModel):
    group_number: Optional[str] = None
    subject: Optional[str] = None
    max_filesize: Optional[int] = None

class FileOut(BaseModel):
    id: int = Field(ge = 1)
    group_number: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    filename: str = Field(min_length=1)
    filesize: int = Field(ge=1)

    model_config = {
        'from_attributes': True
    }

