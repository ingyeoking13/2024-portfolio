from src.models.response.response import Content
from typing import cast, Optional, List
from fastapi import APIRouter, Response, WebSocket
from src.repository.task_job.repo import TaskJobRepo
from src.models.job.task_job import TaskJob
from src.utils.yaml.yaml import load_settings
from src.db.redis_controller import get_redis
from src.ray.utils.actor_child import create_actor
from src.service.algorithm.rate_limiter.limiter import APILimiter
from src.service.algorithm.rate_limiter.token_bucket import TokenBucket
from src.service.algorithm.rate_limiter.leaky_bucket import LeakyBucket
import asyncio

from src.service.algorithm.rate_limiter.limiter import RequestUser
from uuid import uuid4

secret_key = 'my_secret_key' 
expire_minutes = 30

class RateLimiterRouter:
    router = APIRouter(prefix='/v1/rate_limiter')

    @router.post('/token_bucket', response_model=Content)
    async def token_bucket():
        domain, sub_domain = ('rate_limiter', 'token_bucket')
        request_user = RequestUser(str(uuid4()), domain, sub_domain)
        unique_id = await request_user.job(
            load_settings()[domain][sub_domain]['url']
        )
        return Content(data=unique_id)
    
    @router.post('/leaky_bucket', response_model=Content)
    async def leaky_bucket():
        url = load_settings()['rate_limiter']['leaky_bucket']['url']
        unique_id = await create_actor(RequestUser, 
                                       'rate_limiter', 
                                       'leaky_bucket', 
                                       url=url)
        return Content(data=unique_id)
    
    @router.get('', response_model=Content[List[TaskJob]])
    async def result_get(response: Response, 
                               domain: str, sub_domain: Optional[str] = None):
        results = TaskJobRepo().get_job(domain, sub_domain)
        return Content(data=results)

    
    @router.websocket('/status/token_bucket')
    async def token_bucket_status(websocket: WebSocket, id: str):
        r = get_redis(
            **load_settings()['ray']['redis']
        )

        await websocket.accept()
        time = 0
        while True:
            message = await r.xread(
                {id: time}
            )
            if not message:
                continue
            list_data = [
                {
                    'time': data[0].decode().split('-')[0],
                    'name': data[1][b'name'].decode(),
                    'status': data[1][b'status'].decode(),
                    'result': data[1][b'result'].decode(),
                }
                for data in message[0][1]]
            time = int(list_data[-1]['time']) + 1
            await websocket.send_json(list_data)
    
    @router.get('/token_bucket/job')
    @APILimiter(TokenBucket)
    async def token_bucket_job():
        await asyncio.sleep(10)
        return True

    @router.get('/leaky_bucket/job')
    @APILimiter(LeakyBucket)
    async def token_bucket_job():
        # await asyncio.sleep(10)
        return True