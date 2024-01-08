from src.models.response.response import Content
from typing import cast
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

    @router.post('/token_bucket', response_model=Content)
    async def token_bucket():
        url = load_settings()['rate_limiter']['token_bucket']['url']
        unique_id = await create_actor(RequestUser, url=url) 
        return Content(data=unique_id)
    
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
