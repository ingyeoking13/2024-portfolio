from pydantic import BaseModel
from src.utils.yaml.yaml import load_settings
from src.db.redis_controller import get_redis
from typing import Dict
from time import time

class LeakyBucketSetting(BaseModel):
    redis: Dict
    outflow_rate: float
    capacity: int

class LeakyBucket:

    def __init__(self) -> None:
        self.setting: LeakyBucketSetting = \
            LeakyBucketSetting(
                **load_settings()['rate_limiter']['leaky_bucket']
            )
        self.key = 'leaky_bucket'
        self.r = get_redis(**self.setting.redis)

    async def consume(self) -> bool:
        current_time = time()
        last_done, count = await self.r.hmget(
            self.key, 
            ['last_done', 'count']
        )
        last_done = float(last_done or 0)
        count = float(count or 0)

        time_elapsed = current_time - last_done
        conversion_count = time_elapsed * self.setting.outflow_rate

        if max(0, count - conversion_count) < self.setting.capacity:
            await self.r.hset(self.key, mapping={
                'last_done': current_time,
                'count': max(0, count - conversion_count) + 1
            })
            return True
        else:
            return False


