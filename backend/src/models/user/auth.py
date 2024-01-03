from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4

class Auth(BaseModel):
    id: str = Field('')
    name: str = Field('')
    nickname: str = Field('')
    email: str = Field('')
    password: str = Field('')
    salt: str = Field('')

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
