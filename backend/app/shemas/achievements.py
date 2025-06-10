from pydantic import BaseModel, Field
from typing import Optional

class AchieveIn(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default="")
    amount: Optional[int] = Field(default=1)
    image_path: Optional[str] = Field(min_length = 1)
class AchieveID(BaseModel):
    id: int = Field(ge = 1)

class AchieveUpdate(BaseModel):
    id: int = Field(ge = 1)
    name: Optional[str] = Field(min_length=1, max_length=255)
    description: Optional[str]
    amount: Optional[int] = Field(ge=1)
    image_path: Optional[str] = Field(min_length=1)
