from .decorator import async_cache
from .handler import Cache
from .schemas import CacheNamespace

__version__ = '1.0.0'
__all__ = ['async_cache', 'Cache', 'CacheNamespace']
__doc__ = """
    Библиотека кеширования данных через Redis.
    Позволяет кешировать ответ стандартных типов данных, 
    а так-же ответ в виде схемы Pydantic (Необходимо четко указать схему)
    
    Инициализация:
    - Производится при старте сервиса путем вызова класса Cache и метода init,
    куда необходимо передать объект Redis
    Пример:
    ```
    from cache import Cache
    
    redis = Redis(**redis_kwargs)
    Cache.CACHE_PREFIX = "cache"  # Префикс, с которым будут сохранены данные в Redis
    await Cache().init(redis)
    ```
    
    Использование:
    Перед функцией / методом, результат которого необходимо кешировать, поставить декоратор async_cache.
    Параметры: 
        ex: int = 300 - (Необязательный параметр) Время хранения данных в кеше в секундах. default=300
        namespace: CacheNamespace - (Необязательный параметр), имя под которым будут храниться кешированные данные
        model - (Необязательный параметр), Pydantic модель, к которой необходимо привести данные при получении.
        Иначе данные буду приведены к стандартным типам.
        * Если кешируемая функция возвращает Pydantic схему, но в декоратор не передан параметр model, 
        то ответ из кеша будет возвращен в виде dict, что может привести к ошибке в обработке ответа функции.
        * Если функция возвращает пустой список или объект None - то этот ответ не кешируется
    
    Пример использование декоратора:  
    ```
    from cache import async_cache, CacheNamespace
    
    @async_cache(ex=900, namespace=CacheNamespace.ACCOUNT_USER, model: AccountUser)
    def get_user(id: uuid.UUID) -> AccountUser
        ...
        return AccountUser(id=6c3f3f3c-a8c1-4c3e-aa31-be2b1b40d811, name='admin')
    ```
    
    Очистка кеша:
    Очистка кеша производится по: 
    - ключу
    - namespace, если он был передан в декоратор
    - Данным, хранящимся в кеше.
        В данном случае необходимо передать обязательно namespace и search_data
        Если в search_data передать dict (ключ: значение), 
        то будет произведен поиск данных по указанному ключу И значению
    Пример:
    ```
    from cache import Cache, CacheNamespace
    
    # Очистка кеша по namespace
    await Cache().delete_by_namespace(namespace=CacheNamespace.ACCOUNT_USER)
    
    # Очистка кеша по ключу:
    await Cache().delete(key='6c3f3f3c-a8c1-4c3e-aa31-be2b1b40d811')
    
    # Очистка кеша по значениям в кеше:
    await Cache().delete_by_value(namespace=CacheNamespace.ACCOUNT_USER, search_data=str(account_user_id))
    
    await Cache().delete_by_value(
        namespace=CacheNamespace.ACCOUNT_USER, 
        search_data={
            "id": "6c3f3f3c-a8c1-4c3e-aa31-be2b1b40d811"
        }
    )
    ```
"""

