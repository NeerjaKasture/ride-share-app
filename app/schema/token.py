from pydantic import BaseModel
from typing import Optional
from .user import UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str
    uid: int
    name: str
    username: str


class TokenData(BaseModel):
    username: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
