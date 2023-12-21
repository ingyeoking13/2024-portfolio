from typing import Any, Mapping
from pydantic import BaseModel
from fastapi.responses import Response
from starlette.background import BackgroundTask

class Content[T](BaseModel):
    data: T
    error_code: int
    error_message: str

class BasicResponse[T](Response, BaseModel):
    content: Content[T]
    status_code: int
    def __init__(self, content: T = None, 
                 status_code: int = 200, 
                 headers: Mapping[str, str] | None = None, 
                 media_type: str | None = 'application/json', 
                 background: BackgroundTask | None = None) -> None:
        super().__init__(content=content, status_code=status_code, 
                         headers=headers, media_type=media_type, 
                         background=background)


