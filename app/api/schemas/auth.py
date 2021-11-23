from pydantic import BaseModel
from .user import UserCreate


class UserLogin(UserCreate):
    pass


class TokenResponse(BaseModel):
    access_token: str


class AccountResponse(TokenResponse):
    user_id: int
