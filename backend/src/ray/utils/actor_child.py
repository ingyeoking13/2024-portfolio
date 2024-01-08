import ray 
import ray.actor
from typing import cast
from src.ray.utils.actor_center import get_center_actor
from src.db.redis_controller import get_redis
from src.utils.yaml.yaml import load_settings
from src.utils.logger.logger import get_logger
from time import time

_logger = get_logger(__file__, 'ray')

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
        _logger.info(f'{self.key} run')
        await r.xadd(self.key, {
            'name': self.id,
            'result': '',
            'status': 'run'
        })

        result = await self.job(**kwargs)
        
        _logger.info(f'{self.key} fin')
        if self.key == self.id: 
            result = 'fin'
        await r.xadd(self.key, {
            'name': self.id,
            'result': result,
            'status': 'fin'
        })

        return None

async def create_actor(cls: ChildActor, *args, **kwargs):
    centered_actor = get_center_actor()
    unique_id = await centered_actor.push.remote(
        cls, *args, **kwargs
    )
    return unique_id

def call_on_another_worker(args: list[ray.actor.ActorHandle], **kwargs):
    actor_handles = args
    return ray.get([handle.run.remote(**kwargs) for handle in actor_handles])