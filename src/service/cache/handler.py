import hashlib
import inspect
import uuid

import orjson
import jmespath
from typing import Any, Callable, Optional, Type, get_type_hints
from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from redis.asyncio.client import Redis

from service.cache.schemas import CacheNamespace
from utils.utils import PydanticDictModel


class Cache:
    CACHE_PREFIX = 'cache'
    _redis: Optional[Redis] = None

    @classmethod
    async def init(cls, redis: Redis):
        cls._redis = redis

    @staticmethod
    def _is_basic_type(type_hint: Any) -> bool:
        """Проверяет, является ли тип базовым (int, str, float, bool, list, dict и т.д.)."""
        basic_types = (int, str, float, bool, list, dict, tuple, set, type(None), uuid.UUID)
        return isinstance(type_hint, type) and issubclass(type_hint, basic_types)

    @staticmethod
    def _filtered(iterable):
        """Фильтрует None значения из iterable."""
        return filter(lambda x: x is not None, iterable)

    @classmethod
    def _generate_key(cls, func: Callable, namespace: str, *args, **kwargs) -> str:
        type_hints = get_type_hints(func)
        # Фильтруем аргументы, оставляя только базовые типы
        filtered_args = []
        for i, arg in enumerate(args):
            param_name = list(inspect.signature(func).parameters.keys())[i]
            if param_name in type_hints and cls._is_basic_type(type_hints[param_name]):
                filtered_args.append(arg)

        filtered_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, uuid.UUID):
                value = str(value)
            if key in type_hints and cls._is_basic_type(type_hints[key]):
                filtered_kwargs[key] = value

        key_parts = [
            func.__name__,
            namespace,
            orjson.dumps(filtered_args).decode(),
            orjson.dumps(filtered_kwargs).decode()
        ]
        return f'{cls.CACHE_PREFIX}:{hashlib.md5("-".join(cls._filtered(key_parts)).encode()).hexdigest()}:{namespace}'

    @classmethod
    async def serialize(cls, data: Any) -> bytes:
        if isinstance(data, PydanticDictModel):
            if hasattr(data, 'results') and not data.results:
                return orjson.dumps(data.model_dump(mode='json'), default=str)
            return orjson.dumps(data.model_dump(mode='json'), default=str)

        return orjson.dumps(data, default=str)

    @classmethod
    async def _deserialize(cls, data: bytes, model: Type[BaseModel]) -> BaseModel:
        if isinstance(model, ModelMetaclass):
            return model(**orjson.loads(data))
        return orjson.loads(data)

    @classmethod
    async def get(cls, key: str, model: Type[BaseModel]) -> Optional[BaseModel]:
        if cls._redis is None:
            raise RuntimeError("Cache not initialized")

        if (data := await cls._redis.get(key)) is None:
            return

        return await cls._deserialize(data, model)

    @classmethod
    async def set(cls, key: str, value: dict, expire: int):
        if cls._redis is None:
            raise RuntimeError("Cache not initialized")

        serialized_value = await cls.serialize(value)
        await cls._redis.set(key, serialized_value, ex=expire)

    @classmethod
    async def delete(cls, key: str):
        if cls._redis is None:
            raise RuntimeError("Cache not initialized")

        await cls._redis.delete(key)

    @classmethod
    async def delete_by_namespace(cls, namespace: str):
        if cls._redis is None:
            raise RuntimeError("Cache not initialized")

        keys = await cls._redis.keys(f"{namespace}*")
        await cls._redis.delete(*keys)

    @classmethod
    async def delete_by_value(cls, namespace: CacheNamespace, search_data: Any):
        if cls._redis is None:
            raise RuntimeError("Cache not initialized")

        namespace = namespace.value if isinstance(namespace, CacheNamespace) else namespace
        for key in await cls._redis.keys(f"*{namespace}*"):
            if data := await cls._redis.get(key):
                decoded_data = orjson.loads(data)
                if isinstance(decoded_data, dict):
                    # Если decoded_data — словарь, формируем запрос для поиска всех ключей и значений
                    if isinstance(search_data, dict):
                        query = " | ".join(f"{k} == `{v}`" for k, v in search_data.items())
                    else:
                        query = f"contains(values(@), `{search_data}`)"
                elif isinstance(decoded_data, list | type | set):
                    # Если decoded_data — список, ищем совпадение в элементах списка
                    query = f"contains(@, `{search_data}`)"
                else:
                    if search_data in decoded_data:
                        await cls._redis.delete(key)
                    continue

                if jmespath.search(query, decoded_data):
                    await cls._redis.delete(key)
