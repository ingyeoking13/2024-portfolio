import ray 
from typing import cast
from src.ray.utils.actor_center import get_center_actor

class ChildActor:

    def __init__(self) -> None:
        self.parent = None

    async def run(self, **kwargs):
        await self.job(**kwargs)

async def create_actor(cls: ChildActor, **kwargs):
    centered_actor = get_center_actor()
    unique_id = await centered_actor.push.remote(
        cls, **kwargs
    )
    return unique_id
