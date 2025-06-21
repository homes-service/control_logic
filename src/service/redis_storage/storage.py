import asyncio
from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis
from redis.exceptions import (
    ConnectionError,
    ClusterError,
    DataError,
    LockError,
    ReadOnlyError,
    NoScriptError
)
from orjson import orjson, JSONDecodeError

from service.logger.logger import Log
from service.redis_storage import get_redis

log = Log().get_logger(__name__)


class AsyncRedisStorage:
    TIMEOUT_EXPIRATION = 20

    _EXCEPTIONS = ConnectionError, ClusterError, DataError, LockError, ReadOnlyError, NoScriptError

    def __init__(self, redis: Redis | None = None):
        self.redis = redis

        self.time_spend = 0
        self.start_sleep_time: float = 0.1
        self.factor: int = 2
        self.border_sleep_time: int = 5

    async def __aenter__(self):
        self.redis = await get_redis()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def _exception(self):
        log.warning('Connecting to Redis loss...')
        if self.time_spend < self.border_sleep_time:
            self.time_spend += self.start_sleep_time * pow(2, self.factor)
        if self.time_spend >= self.border_sleep_time:
            self.time_spend = self.border_sleep_time
        log.debug(f'Time waiting: {self.time_spend}')
        await asyncio.sleep(self.time_spend)

    @staticmethod
    def _backoff(function):
        async def wrapper(self, *args, **kwargs):
            while True:
                try:
                    return await function(self, *args, **kwargs)
                except self._EXCEPTIONS:
                    await self._exception()
        return wrapper

    @_backoff
    async def set_message(self, message_id: str, message: str | dict, ex: int = None):
        if isinstance(message, dict):
            message = await asyncio.to_thread(orjson.dumps, message, default=str)
        await self.redis.set(message_id, message, ex=ex)

    @_backoff
    async def get_message(self, message_id: str) -> str | dict | None:
        result = await self.redis.get(message_id)
        try:
            return orjson.loads(result)
        except JSONDecodeError:
            if isinstance(result, bytes):
                return result.decode("utf-8")
            return result
        except TypeError:
            return None

    @_backoff
    async def delete_message(self, message_id: str):
        return await self.redis.delete(message_id)

    async def get_keys(self, prefix_key):
        while True:
            try:
                for key in await self.redis.keys(f'*{prefix_key}*'):
                    yield key, await self.get_message(key)
            except self._EXCEPTIONS:
                await self._exception()
            else:
                break

    @_backoff
    async def is_message(self, message_id: str):
        if await self.redis.get(message_id) and await self.redis.ttl(message_id) > 3:
            return True
        return False

    @_backoff
    async def get_ttl(self, message_id: str):
        return await self.redis.ttl(message_id)

    @_backoff
    async def set_expire_message(self, message_id, ex: int):
        """ Продлить время хранения данных """
        await self.redis.expire(message_id, ex)


@lru_cache()
def redis_service(redis: Redis = Depends(get_redis)) -> AsyncRedisStorage:
    return AsyncRedisStorage(redis)
