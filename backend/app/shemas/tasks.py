from uuid import UUID

from pydantic import BaseModel, root_validator, Field
from typing import Optional
from datetime import datetime

class TaskIn(BaseModel):
    user_id: int = Field(ge = 1)
    deadline: Optional[datetime] = None
    description: Optional[str] = Field(min_length=1, default=None)
    task_flag: Optional[int] = Field(ge=0, le=3, default=0)


class TaskInShort(BaseModel):
    deadline: Optional[datetime] = None
    description: Optional[str] = Field(min_length=1, default=None)
    task_flag: Optional[int] = Field(ge=0, le=3, default=0)

class TaskID(BaseModel):
    task_id: int =  Field(ge = 1)

class TaskUpdate(BaseModel):
    task_id: int = Field(ge=1)
    deadline: Optional[datetime] = None
    description: Optional[str] = Field(min_length=1, default=None)
    task_flag: Optional[int] = Field(ge=0, le=3, default=0)

class SharedLinkIn(BaseModel):
    task_id: int = Field(ge = 1)
    user_id: int = Field(ge = 1)
    expires_at: Optional[datetime] = None

class SharedLinkOut(SharedLinkIn):
    id: int = Field(ge = 1)
    token: UUID