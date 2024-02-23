import ray
import aiohttp
from src.repository.actor_job.repo import ActorJobRepo
from src.models.job.actor_job import ActorJob
from src.ray.utils.actor_child import (
    ChildActor, create_actor, call_on_another_worker
)
from datetime import datetime
from uuid import uuid4


@ray.remote(num_cpus=0.1)
class RequestUser(ChildActor):
    def __init__(self, id, domain, sub_domain) -> None:
        super().__init__(id)
        self.type = 'RequestUser'
        self.domain = domain
        self.sub_domain = sub_domain

    async def job(self, url):
        actor_clses = []
        repo = ActorJobRepo()
        job = ActorJob(
            name=self.id,
            parent_name='',
            start_time=datetime.now(),
            type=self.type,
            domain=self.domain,
            sub_domain=self.sub_domain
        )
        repo.add_job( 
            job
        )

        for _ in range(50):
            id = str(uuid4())
            actor_clses.append(RequestChildUser.options(
                    name=id
                ).remote(id, self.id)
            )

        results = await call_on_another_worker(actor_clses, url=url)
        job.result = {
            'result': results
        } 
        job.end_time = datetime.now()

        repo.set_result(
            job
        )

        return (self.id, results)

@ray.remote(num_cpus=0.2)
class RequestChildUser(ChildActor):
    def __init__(self, id, parent_id) -> None:
        super().__init__(id, parent_id)
    
    async def job(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status
