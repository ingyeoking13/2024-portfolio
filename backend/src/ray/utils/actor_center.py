import ray
import ray.actor
from typing import List
from uuid import uuid4
from queue import Queue
import asyncio
from src.db.redis_controller import get_redis
from src.utils.yaml.yaml import load_settings
from time import time

@ray.remote
class CenteredActor:
    def __init__(self) -> None:
        self.waiting_queue:Queue = Queue()
        self.running_handles:List[ray.ObjectRef] = []
        self.cond = asyncio.Condition()

    async def running(self):
        r = get_redis(
            **load_settings()['ray']['redis']
        )
        while True:
            async with self.cond:
                finished_items, waitings =\
                    ray.wait(self.running_handles, timeout=0.1)
                await asyncio.sleep(0.1)
                self.running_handles = waitings

                if finished_items:
                    for fin_item in finished_items:
                        await r.zadd(f'{fin_item}', {
                            'fin': time()
                        })


    async def watch(self):
        r = get_redis(
            **load_settings()['ray']['redis']
        )
        while True:
            await asyncio.sleep(0.1)
            try:
                id, ray_instance, kwargs = self.waiting_queue.get(
                    block=False
                )
            except:
                continue
            running_handle = ray_instance.run.remote(
                **kwargs
            )
            await r.zadd(f'{running_handle}', {
                'run': time()
            })
            async with self.cond:
                self.running_handles.append(running_handle)

    async def push(self, ray_handle: ray.actor.ActorClass,
                   **kwargs
                   ):
        id = str(uuid4())
        ray_instance = ray_handle.options(
            name=id,
            num_cpus=0.1
        ).remote()
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
        instance.running.remote()
        handle = ray.get_actor('CenteredActor')
    return handle


get_center_actor()