from datetime import datetime
from pydantic import BaseModel, Field

class TaskJob(BaseModel):
    name: str = Field('')
    parent_name: str = Field('')
    domain: str = Field('')
    sub_domain: str = Field('')
    start_time: datetime = Field() 
    end_time: datetime = Field(datetime(9999,12,31))
    type: str = Field('')
    result: dict = Field('')

    class Config:
        from_attributes = True
