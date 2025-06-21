import functools
from typing import Optional, Type, Callable

from pydantic import BaseModel

from service.cache.handler import Cache
from service.cache.schemas import CacheNamespace


def async_cache(
        ex: int = 300,
        namespace: CacheNamespace = CacheNamespace.ANY,
        model: Optional[Type[BaseModel]] = None,
):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = Cache._generate_key(func, namespace.value, *args, **kwargs)
            if cached_result := await Cache.get(key, model):
                return cached_result

            result = await func(*args, **kwargs)
            if result is None:
                return result

            await Cache.set(key, result, ex)
            return result

        return wrapper

    return decorator
