from typing import Optional
from pydantic import BaseModel


class BaseUser(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None


class UserCreate(BaseUser):
    username: str
    password: str


class UserEdit(BaseUser):
    password: Optional[str] = None
