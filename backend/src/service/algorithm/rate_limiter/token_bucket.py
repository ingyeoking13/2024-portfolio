from pydantic import BaseModel
from math import floor
from typing import Dict, List
from src.utils.yaml.yaml import load_settings
from src.db.redis_controller import get_redis
from time import time

class TokenBucketSetting(BaseModel):
    redis: Dict 
    fill_rate: int
    capacity: int

class TokenBucket:
    """
    토큰 버킷 알고리즘
    토큰 공급률 : 1분에 30개 (settings.yaml의 fill_rate 참조)
    토큰 캐파: 60개
    """
    def __init__(self) -> None:
        self.setting: TokenBucketSetting = \
            TokenBucketSetting(
                **load_settings()['rate_limiter']['token_bucket'])
        self.key = 'token_bucket'
        self.time_key = 'token_bucket_time'
        self.r = get_redis(**self.setting.redis)
    
    def _can_refill(self, last_update_time, now_time):
        if last_update_time == 0:
            return True
       
        if last_update_time - now_time > 60:
            return True

        return False
    
    async def _refill(self):
        last_update_time = floor(float(await self.r.get(self.time_key) or 0))
        # 만약 60 초 이상이라면 토큰을 공급한다.
        if self._can_refill(last_update_time, time()):
            if last_update_time == 0:
                await self.r.set(self.key, self.setting.capacity)
            else:
                current_token = int(await self.r.get(self.key) or 0)
                await self.r.set(
                    current_token,
                    min(self.setting.capacity, 
                            current_token + self.setting.fill_rate)
                )
            await self.r.set(self.time_key, time())
    
    async def consume(self) -> bool:
        await self._refill()
        current_token = int(await self.r.get(self.key))
        if current_token <= 0:
            return False
        await self.r.decrby(self.key, 1)
        return True

