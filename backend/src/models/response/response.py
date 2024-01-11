from pydantic import BaseModel, Field
from typing import TypeVar, Generic

T = TypeVar('T')

class Content(BaseModel, Generic[T]):
    data: T
    error_code: int = Field(0)
    error_message: str = Field('')
