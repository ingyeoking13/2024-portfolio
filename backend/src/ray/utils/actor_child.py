import ray 
from typing import cast
from src.ray.utils.actor_center import get_center_actor

class ChildActor:

    def __init__(self) -> None:
        self.parent = None
        self._status = 15

    async def run(self, **kwargs):
        result = await self.job(**kwargs)

    def status(self):
        return self._status

async def create_actor(cls: ChildActor, **kwargs):
    centered_actor = get_center_actor()
    unique_id = await centered_actor.push.remote(
        cls, **kwargs
    )
    return unique_id
