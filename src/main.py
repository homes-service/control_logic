from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI, Response, Request
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from service.exc import *
from service import redis_storage
from service.cache import Cache

from service.logger import Log
from settings import settings
from api.routers import all_routers
from settings import settings

log = Log.get_logger(__name__)



origins = [
    "http://localhost:5173",
    "202.181.148.110",
    "http://10.8.0.10:8000",
    "10.8.0.3",
    "http://localhost:8000",
    "http://192.168.31.206:8000"
]
middleware_kwargs = {
    'allow_origins': origins,
    'allow_credentials': True,
    'allow_methods': ["*"],
    'allow_headers': ["*"]
}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Инициализация Redis
    redis_kwargs = {'host': settings.REDIS_HOST, 'port': settings.REDIS_PORT}
    redis_storage.redis = Redis(**redis_kwargs)

    # Инициализация кеширования
    Cache.CACHE_PREFIX = "cache"
    await Cache().init(redis_storage.get_redis())

    yield


app = FastAPI(
    title=f'{settings.MICROSERVICE_NAME} API',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    docs_url=f"{settings.SERVICE_PREFIX}/docs",
    openapi_url=f"{settings.SERVICE_PREFIX}/openapi.json",

)

for router in all_routers:
    app.include_router(router)


app.add_middleware(CORSMiddleware, **middleware_kwargs)

# === РЕГИСТРАЦИЯ ИСКЛЮЧЕНИЙ === #
app.add_exception_handler(NotFoundError, not_found_404)
app.add_exception_handler(BadRequestError, bad_request_400)
app.add_exception_handler(ExistDataError, bad_request_400)
app.add_exception_handler(PermissionDeniedError, forbidden_403)
app.add_exception_handler(AuthorizationError, unauthorized_401)
app.add_exception_handler(Exception, exception_500)



@app.middleware("http")
async def add_custom_headers_and_cookies(request: Request, call_next):
    # TODO: Для тестирования. Принтует заголовки отправляемые клиенту
    response: Response = await call_next(request)
    # print(f'{response.status_code=}')
    if response.status_code == status.HTTP_200_OK:
        print(f'***** 200 OK: {response.headers=}')
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        print(f'***** 401: {response.headers=}')
    if response.status_code == 500:
        print(f'***** 417: {response.headers=}')
    return response


if settings.IS_UVICORN_WORK_SERVER and __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)
