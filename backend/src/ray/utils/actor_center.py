import ray
import ray.actor
from typing import List
from uuid import uuid4
from queue import Queue
import asyncio
from src.utils.logger.logger import get_logger

_logger = get_logger(__file__, 'ray')

@ray.remote
class CenteredActor:
    def __init__(self) -> None:
        self.waiting_queue:Queue = Queue()
        self.running_handles:List[ray.ObjectRef] = []
        self.cond = asyncio.Condition()

    async def watch(self):
        while True:
            await asyncio.sleep(0.1)
            try:
                id, ray_instance, kwargs = self.waiting_queue.get(
                    block=False
                )
            except:
                continue
            (actor_id, result)= ray.get(ray_instance.run.remote(
                **kwargs
            ))
            ray.kill(actor_id)


    async def push(self, ray_cls: ray.actor.ActorClass,
                   *args, **kwargs
                   ):
        id = str(uuid4())
        ray_instance = ray_cls.options(
            name=id,
            num_cpus=0.1
        ).remote(id, *args)
        async with self.cond:
            self.waiting_queue.put((id,ray_instance, kwargs))
        return id

def get_center_actor():
    try:
        handle = ray.get_actor('CenteredActor')
    except:
        instance = CenteredActor.options(
            name='CenteredActor', lifetime='detached'
        ).remote()
        instance.watch.remote()
        # instance.running.remote()
        handle = ray.get_actor('CenteredActor')
    return handle

get_center_actor()