import ray 
import ray.actor
from src.ray.utils.actor_center import get_center_actor
from src.db.redis_controller import get_redis
from src.utils.yaml.yaml import load_settings
from src.utils.logger.logger import get_logger

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
        start = ''
        if self.key == self.id: 
            start = 'start'
        await r.xadd(self.key, {
            'name': self.id,
            'result': start,
            'status': 'run'
        })

        result = await self.job(**kwargs)
        
        _logger.info(f'{self.key} fin')
        await r.xadd(self.key, {
            'name': self.id,
            'result': (
                'fin' if self.key == self.id
                else 'done'
            ),
            'status': 'fin'
        })

        return (self.id, result)

async def create_actor(cls: ChildActor, *args, **kwargs):
    centered_actor = get_center_actor()
    unique_id = await centered_actor.push.remote(
        cls, *args, **kwargs
    )
    return unique_id

async def call_on_another_worker(args: list[ray.actor.ActorHandle], **kwargs):
    actor_handles = args
    running = [
        handle.run.remote(**kwargs)
        for handle in actor_handles
    ]
    results = []
    while running:
        fin, unfin = ray.wait(running)
        running = unfin
        for _fin in fin:
            actor_id, result = ray.get(_fin)
            ray.kill(ray.get_actor(actor_id))
            results.append(result)

    return results
