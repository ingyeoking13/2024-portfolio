import ray
import asyncio
import aiohttp
import requests
from src.ray.utils.actor_child import ChildActor

@ray.remote(num_cpus=0.1)
class RequestUser(ChildActor):
    def __init__(self):
        pass

    async def job(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(response.status)
                return response.status
