import ray
import ray.actor
from typing import List
from uuid import uuid4
from queue import Queue
import asyncio

@ray.remote
class CenteredActor:
    def __init__(self) -> None:
        self.waiting_queue:Queue = Queue()
        self.running_handles:List[ray.ObjectRef] = []

    async def running(self):
        count = 0
        await asyncio.sleep(0.1)
        finisehd, waitings = ray.wait(self.running_handles)
        self.running_handles = waitings
        count += 1
        print('^^', count)
        return finisehd

    async def watch(self):
        count = 0
        while True:
            await asyncio.sleep(0.1)
            try:
                id, ray_instance, kwargs = self.waiting_queue.get(
                    block=False
                )
            except:
                continue
            count += 1
            print(count)
            running_handle = ray_instance.run.remote(
                **kwargs
            )
            self.running_handles.append(running_handle)
            await self.running()

    async def push(self, ray_handle: ray.actor.ActorClass,
                   **kwargs
                   ):
        id = str(uuid4())
        ray_instance = ray_handle.options(
            name=id
        ).remote()
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
        handle = ray.get_actor('CenteredActor')
    return handle


get_center_actor()