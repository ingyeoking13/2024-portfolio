from src.models.response.response import Content
from fastapi import APIRouter, Depends, Cookie, Response, WebSocket
from datetime import datetime, timedelta
from src.utils.yaml.yaml import load_settings
from src.db.redis_controller import get_redis
from src.ray.utils.actor_child import create_actor
import asyncio
import ray

from src.ray.rate_limiter.index import RequestUser

secret_key = 'my_secret_key' 
expire_minutes = 30

class RateLimiterRouter:
    router = APIRouter(prefix='/v1/rate_limiter')

    @router.post('/token_bucket')
    async def token_bucket():
        url = load_settings()['rate_limiter']['token_bucket']['url']
        unique_id = await create_actor(RequestUser, url=url) 
        return unique_id
    
    @router.get('/token_bucket')
    async def token_bucket_get(response: Response):
        r = get_redis(
            **load_settings()['rate_limiter']['token_bucket']['redis']
        )
        val = await r.get('token_bucket') or 0
        if int(val) >= 15:
            response.status_code = 429
            return False

        await r.incrby('token_bucket')

        await asyncio.sleep(10)
        result = True

        await r.decrby('token_bucket')
        return result
    
    @router.websocket('/status/token_bucket')
    async def token_bucket_status(websocket: WebSocket, id: str):
        r = get_redis(
            **load_settings()['rate_limiter']['token_bucket']['redis']
        )
        await websocket.accept()
        r.xgroup_create(id, groupname=f'g-{id}')
        while True:
            message = r.xreadgroup(f'g-{id}', f'c-{id}', {'stream': '>'})
            print(message)
            r.xack(id, f'g-{id}',message[1])
            await websocket.send_text(message)

