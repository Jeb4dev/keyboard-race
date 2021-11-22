from typing import Optional
from pydantic import BaseModel


class BaseUser(BaseModel):
    id: Optional[int]
    username: Optional[str]


class UserCreate(BaseUser):
    username: str
    password: str


class UserEdit(BaseUser):
    password: Optional[str]
