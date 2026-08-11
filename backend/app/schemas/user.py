from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
