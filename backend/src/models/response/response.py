from typing import Any, Mapping
from typing_extensions import Unpack
from pydantic import BaseModel, Field
from fastapi.responses import Response
from pydantic.config import ConfigDict
from starlette.background import BackgroundTask

class Content[T](BaseModel):
    data: T
    error_code: int = Field(0)
    error_message: str = Field('')

class BasicResponse[T](Response):
    def __init__(self, content: T = None, 
                 status_code: int = 200, 
                 headers: Mapping[str, str] = {
                     'Content-Type': 'application/json'},
                 media_type: str | None = None, 
                 background: BackgroundTask | None = None) -> None:
        super().__init__(content.json(), status_code, headers, media_type, background)

