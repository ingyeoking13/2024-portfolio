from src.models.response.response import Content
from fastapi import APIRouter, Depends, Cookie
from datetime import datetime, timedelta
from src.utils.yaml.yaml import load_settings
import ray

from src.ray.rate_limiter.index import RequestUser

secret_key = 'my_secret_key' 
expire_minutes = 30

class RateLimiterRouter:
    router = APIRouter(prefix='/v1/rate_limiter')

    @router.post('/token_bucket')
    async def token_bucket():
        handle = RequestUser().task.remote(
            url= load_settings()['algorithm_url']['token_bucket']
        )
        ray.get(handle)
    
    @router.get('/token_bucket')
    async def token_bucket_get():
        return True
    
    @router.get('/status/token_bucket')
    async def token_bucket_status():
        pass


