import ray
import asyncio
import aiohttp
import requests
from src.ray.utils.actor_child import (
    ChildActor, create_actor, call_on_another_worker
)
from uuid import uuid4


@ray.remote(num_cpus=0.1)
class RequestUser(ChildActor):
    def __init__(self, id) -> None:
        super().__init__(id)

    async def job(self, url):
        results = []
        clses = []
        for _ in range(1000):
            clses.append(RequestChildUser.remote(str(uuid4()), self.id))

        call_on_another_worker(clses, url=url)

        return results

@ray.remote(num_cpus=1)
class RequestChildUser(ChildActor):
    def __init__(self, id,parent_id) -> None:
        super().__init__(id, parent_id)
    
    async def job(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status
