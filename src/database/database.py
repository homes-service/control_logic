from typing import AsyncGenerator

from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.exc import IllegalStateChangeError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from service.logger.logger import Log
from settings import settings


log = Log().get_logger(__name__)

kwargs_engine = {
    'logging_name': 'db_InteractionService',
    'poolclass': AsyncAdaptedQueuePool,
    'max_overflow': 20,  # количество дополнительных соединений
    'pool_size': 40,     # базовое количество соединений в пуле
    'future': True,
    'echo': False,
}

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), **kwargs_engine)
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session() as session:
            yield session
    except IllegalStateChangeError as error:
        log.critical(f'*** !!! SQL SESSION ERROR !!! ***: {str(error)}')
        await session.rollback()
        await session.close()
