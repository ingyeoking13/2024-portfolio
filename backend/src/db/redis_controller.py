import redis.asyncio as redis

def get_redis(**settings) -> redis.Redis:
    return redis.Redis(**settings)