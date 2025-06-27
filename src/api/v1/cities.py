from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


from database import get_session
from settings import settings

router = APIRouter(
    prefix=f"{settings.V1}/cities",
    tags=["List of cities"],
)

@router.get(
    "/",
    response_model=List[CitiesGroup],
    summary="Получить список городов"
)
async def get_all_cities(
    db: AsyncSession = Depends(get_session),
):



@router.post(
    "/new_city",
    response_model=List[CitiesGroup],
    summary="Добавить новый город"
)
async def add_new_city(
    db: AsyncSession = Depends(get_session),
):
    


@router.patch(
    "/change_city",
    response_model=List[CitiesGroup],
    summary="Изменить список городов"
)
async def change_cities(
    db: AsyncSession = Depends(get_session),
):