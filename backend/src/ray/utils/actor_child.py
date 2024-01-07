import ray 
from typing import cast
from src.ray.utils.actor_center import get_center_actor
from src.db.redis_controller import get_redis
from src.utils.yaml.yaml import load_settings
from time import time

class ChildActor:

    def __init__(self, id, parent_id = None) -> None:
        self.parent = None
        self.id = id
        self.parent_id = parent_id
    
    @property
    def key(self):
        return self.parent_id or self.id 

    async def run(self, **kwargs):
        r = get_redis(
            **load_settings()['ray']['redis']
        )
        await r.xadd(self.key, {
            'name': self.id,
            'result': '',
            'status': 'run'
        })

        result = await self.job(**kwargs)
        
        await r.xadd(self.key, {
            'name': self.id,
            'result': result,
            'status': 'run'
        })

async def create_actor(cls: ChildActor, *args, **kwargs):
    centered_actor = get_center_actor()
    unique_id = await centered_actor.push.remote(
        cls, *args, **kwargs
    )
    return unique_id
