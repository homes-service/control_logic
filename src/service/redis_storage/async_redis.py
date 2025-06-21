from functools import lru_cache

from redis.asyncio import Redis

redis: Redis | None = None


@lru_cache
async def get_redis() -> Redis:
    return redis
