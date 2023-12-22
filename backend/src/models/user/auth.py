from pydantic import BaseModel, Field
from typing import Optional

class Auth(BaseModel):
    id: str
    name: str
    nickname: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
