from src.models.response.response import Content
from typing import cast, Optional, List
from fastapi import APIRouter, Response, WebSocket
from src.repository.actor_job.repo import ActorJobRepo
from src.models.job.actor_job import ActorJob
from src.utils.yaml.yaml import load_settings
from src.db.redis_controller import get_redis
from src.ray.utils.actor_child import create_actor
from src.service.algorithm.rate_limiter.limiter import APILimiter
from src.service.algorithm.rate_limiter.token_bucket import TokenBucket
from src.service.algorithm.rate_limiter.leaky_bucket import LeakyBucket
import asyncio
import ray

from src.ray.id_gen.index import IdGenUser

secret_key = 'my_secret_key' 
expire_minutes = 30

class IdGenRouter:
    router = APIRouter(prefix='/v1/id_gen')

    @router.post('', response_model=Content)
    async def token_bucket():
        unique_id = await create_actor(IdGenUser, 'id_gen', '')
        return Content(data=unique_id)
    
    @router.get('', response_model=Content[List[ActorJob]])
    async def result_get(response: Response, 
                               domain: str, sub_domain: Optional[str] = None):
        results = ActorJobRepo().get_job(domain, sub_domain)
        return Content(data=results)