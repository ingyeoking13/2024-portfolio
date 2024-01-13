import ray
from src.repository.actor_job.repo import ActorJobRepo
from src.service.id_gen.id_gen import IdGenerator, Id
from src.models.job.actor_job import ActorJob
from src.ray.utils.actor_child import (
    ChildActor, create_actor, call_on_another_worker
)
from src.utils.dumps import default_serializer
from functools import reduce
from datetime import datetime
from uuid import uuid4


@ray.remote(num_cpus=0.1)
class IdGenUser(ChildActor):
    def __init__(self, id, domain, sub_domain) -> None:
        super().__init__(id)
        self.type = 'IdGenUser'
        self.domain = domain
        self.sub_domain = sub_domain

    async def job(self):
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
        repo.add_job(job)

        for idx, _ in enumerate(range(10)):
            id = str(uuid4())
            actor_clses.append(IdGenChildUser.options(
                    name=id
                ).remote(id, self.id, 0, idx)
            )

        results = await call_on_another_worker(actor_clses)
        flattened_list = list(reduce(lambda a,b: a+b, results)) 
        job.result = {
            'result': (
                True if len(flattened_list) == len(set(flattened_list)) 
                else False
                )
        } 
        job.end_time = datetime.now()
        repo.set_result(job)

        return (self.id, results)

@ray.remote(num_cpus=0.2)
class IdGenChildUser(ChildActor):
    def __init__(self, id, parent_id, 
                 data_center, server_id) -> None:
        super().__init__(id, parent_id)
        self.generator = IdGenerator(data_center, server_id)
    
    async def job(self):
        result = []
        
        for _ in range(200000):
            id = self.generator.gen_id()
            result.append(f'{id}')
        return result
