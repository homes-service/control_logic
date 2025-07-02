from http.client import HTTPException
import uuid

from api.dependencies import UOWDep
from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.cities import CitySchemaAdd, CitySchema, CitySchemaUpdate
from service.cities import CitiesService

from database import get_session
from settings import settings

router = APIRouter(
    prefix=f"{settings.V1}/cities",
    tags=["List of cities"],
)

@router.get(
    "/{city_id}",
    response_model=CitySchema,
    summary="Получить город по id"
)
async def get_city_by_id(
    city_id: uuid.UUID,
    uow: UOWDep,
):
    city = await CitiesService().get_city_by_id(city_id, uow)
    if not city:
        raise HTTPException(
            status_code=404,
            detail={"success": False, "message": "City not found"}
        )
    return city


@router.post(
    "/",
    response_model=dict,
    summary="Добавить новый город",
    description="Создает запись о городе в базе данных"
)
async def add_city(
    city: CitySchemaAdd,
    uow: UOWDep,
)-> dict:
    city_id = await CitiesService().add_city(uow, city)
    return{
        "success": True,
        "message": "Город успешно добавлен",
        "data": {"city_id": city_id}
    }
    

@router.patch(
    "/{city_id}",
    response_model=CitySchema,
    summary="Изменить город"
)
async def patch_city(
    city_id: uuid.UUID,
    update_data: CitySchemaUpdate,
    uow: UOWDep
):
    city = await CitiesService().update_city(uow, city_id, update_data)
    return city