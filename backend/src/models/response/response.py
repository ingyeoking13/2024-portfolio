from pydantic import BaseModel, Field
from typing import TypeVar

T = TypeVar('T')

class Content(BaseModel):
    data: T
    error_code: int = Field(0)
    error_message: str = Field('')
