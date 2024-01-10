import ray
import aiohttp
from src.ray.utils.actor_child import (
    ChildActor, create_actor, call_on_another_worker
)
from uuid import uuid4


@ray.remote(num_cpus=0.1)
class RequestUser(ChildActor):
    def __init__(self, id) -> None:
        super().__init__(id)

    async def job(self, url):
        actor_clses = []
        for _ in range(500):
            id = str(uuid4())
            actor_clses.append(RequestChildUser.options(
                    name=id
                ).remote(id, self.id)
            )

        results = await call_on_another_worker(actor_clses, url=url)
        return (self.id, results)

@ray.remote(num_cpus=1)
class RequestChildUser(ChildActor):
    def __init__(self,id,parent_id) -> None:
        super().__init__(id, parent_id)
    
    async def job(self, url):
        import requests
        return requests.get(url).status_code
        # async with aiohttp.ClientSession() as session:
            # async with session.get(url) as response:
                # return response.status
