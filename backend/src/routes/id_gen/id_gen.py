from src.models.response.response import Content
from typing import cast, Optional, List
from fastapi import APIRouter, Response, WebSocket
from src.repository.task_job.repo import TaskJobRepo
from src.models.job.task_job import TaskJob
from src.ray.utils.actor_child import create_actor

from src.ray.id_gen.index import IdGenUser

secret_key = 'my_secret_key' 
expire_minutes = 30

class IdGenRouter:
    router = APIRouter(prefix='/v1/id_gen')

    @router.post('', response_model=Content)
    async def token_bucket():
        unique_id = await create_actor(IdGenUser, 'id_gen', '')
        return Content(data=unique_id)
    
    @router.get('', response_model=Content[List[TaskJob]])
    async def result_get(response: Response, 
                               domain: str, sub_domain: Optional[str] = None):
        results = TaskJobRepo().get_job(domain, sub_domain)
        return Content(data=results)