from typing import Any

from fastapi import Request

import orjson
from pydantic import BaseModel


class PydanticDictModel(BaseModel):
    """
    Переопределение базовой модели pydantic BaseModel
    Для замены сериализации объектов библиотекой json на orjson.
    Все схемы наследовать от текущего класса
    """

    class Config:
        json_loads_kwargs = {'object_hook': orjson.loads}
        json_dumps_kwargs = {
            'default': lambda v, *, default:
            orjson.dumps(v, default=default).decode()
        }
        from_attributes = True


def model_dump(model: PydanticDictModel, *args, **kwargs) -> dict[str, Any]:
    """ Преобразование Pydantic модели в объект json """
    return model.model_dump(*args, **kwargs)


async def get_request_body(request: Request) -> dict | None:
    """ Забирает объект body из Request """
    try:
        body = None
        if request.method in ('POST', 'PATCH', 'PUT'):
            if 'multipart/form-data' in request.headers.get('content-type'):
                body_ = await request.form()
                body = body_.__dict__.get('_dict')
            elif 'application/json' in request.headers.get('content-type'):
                body = await request.json()
        return body
    except:
        pass
