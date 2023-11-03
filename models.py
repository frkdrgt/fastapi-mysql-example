from pydantic import BaseModel
from uuid import UUID,uuid4
from typing import Optional
from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"

class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name:str
    gender: Gender


class UserUpdateRequest(BaseModel):
    first_name: str
    last_name:str
    gender: Gender