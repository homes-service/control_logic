from .async_redis import get_redis, redis
from .storage import redis_service, AsyncRedisStorage

__all__ = ['get_redis', 'redis_service', 'AsyncRedisStorage', 'redis']
__version__ = '1.0.0'
__doc__ = """
    Инициализация:
    ```
    from redis_storage import async_redis
    
    redis_kwargs = {'host': settings.REDIS_HOST, 'port': settings.REDIS_PORT}
    async_redis.redis = Redis(**redis_kwargs)
    ```
    Использование:
    ```
    from redis_storage import AsyncRedisStorage
    
    async with AsyncRedisStorage() as storage:
        await storage.set_message(message_id='123', message={"text": "Hello World"}, ex=300)  # Записать в Redis
        result = await storage.get_message(message_id='123')  # Получить сообщение из Redis по id
        await storage.delete_message(message_id='123')  # Удалить сообщение из Redis
        is_message = await storage.is_message(message_id='123')  # Проверка наличия ключа в Redis
        ttl = await storage.get_ttl(message_id='123')  # Остаток хранения ключа в Redis
        await storage.set_expire_message(message_id='123', ex=300)  # Продлить время на хранения
        
        Получить список в виде ключ: значение элементов в Redis, по части ключа. Используется асинхронный генератор
        async for key, value in storage.get_keys(prefix_key='12'):
            print(f'{key=} | {value=})
    ```
"""

