from typing import Any

from pydantic import model_validator, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 7000
    IS_UVICORN_WORK_SERVER: bool = True
    MICROSERVICE_NAME: str = Field(description='Наименование микросервиса', default='Homes service')

    SERVICE_PREFIX: str = "/homes"
    V1_PREFIX: str = "/v1"

    V1: str = f"{SERVICE_PREFIX}{V1_PREFIX}"

    # === Настройки безопасности === #

    # === Redis === #
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379

    # === База данных === #
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: int = 9999
    POSTGRES_USER: str = "homes_user0"
    POSTGRES_PASSWORD: str = "123456789"
    POSTGRES_DB: str = "homes_db0"
    SQLALCHEMY_DATABASE_URI: str = None

    # ===  AUTH Telegram Bot ===
    AUTH_BOT_TOKEN: str = "AuthTelegramBotToken"
    URL_HOME_SERVICE: str = "http://localhost:9000"

    # === NOTIFY Telegram Bot ===
    NOTIFY_BOT_TOKEN: str = "NotifyTelegramBotToken"

    @model_validator(mode='before')
    @classmethod
    def get_sqlalchemy_database_uri(cls, data: dict | Any) -> dict | Any:
        # print(data)
        data.setdefault(
            'SQLALCHEMY_DATABASE_URI',
            f'postgresql+asyncpg://'
            f'{data.get("POSTGRES_USER")}:{data.get("POSTGRES_PASSWORD")}'
            f'@{data.get("POSTGRES_SERVER")}:{data.get("POSTGRES_PORT")}'
            f'/{data.get("POSTGRES_DB")}'
        )
        return data


settings = Settings(_env_file='../.env', _env_file_encoding='utf-8')
# settings = Settings(_env_file='.env', _env_file_encoding='utf-8')