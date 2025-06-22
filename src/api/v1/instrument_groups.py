import uuid

from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import status

from api.dependencies import UOWDep
from schemas.instrument_groups import InstrumentGroupsSchemaAdd, \
    InstrumentGroupSchemaUpdate, InstrumentGroupsSchema, \
    InstrumentGroupsSchemaAddResponse
from service.instrument_groups.instrument_groups import InstrumentGroupsService
from settings import settings

router = APIRouter(
    prefix=f"{settings.V1}/instrument_groups",
    tags=["Instrument Groups"],
)


@router.post(
    "/",
    response_model=dict,
    summary="Добавить группу инструментов",
)
async def add_group(
        group: InstrumentGroupsSchemaAdd,
        uow: UOWDep,
) -> dict:
    group_id = await InstrumentGroupsService().add_group(uow, group)
    result = {
        "success": True,
        "message": "Группа инструментов успешно создана",
        "data": {"instrument_group_id": group_id}
    }
    return result


@router.get(
    "/groups/{account_id}",
    response_model=List[InstrumentGroupsSchema],
    summary="Получить список групп инструментов " \
            "аккаунта (счета)",
)
async def get_groups(
        account_id: uuid.UUID,
        uow: UOWDep,
):
    groups = await InstrumentGroupsService().get_groups(
        uow, account_id=account_id
    )
    if not groups:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "message": "Group not found"}
        )
    return groups


@router.get(
    "/{group_id}",
    response_model=InstrumentGroupsSchema,
    summary="Получить группу инструментов по id",
)
async def get_group_by_id(
        group_id: uuid.UUID,
        uow: UOWDep,
):
    group = await InstrumentGroupsService().get_group_by_id(
        group_id=group_id, uow=uow
    )
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "message": "Instrument group not found"}
        )
    return group


@router.patch(
    '/{group_id}',
    response_model=InstrumentGroupsSchema,
    summary="Изменить группу инструментов"
)
async def path_group(
        group_id: uuid.UUID,
        update_data: InstrumentGroupSchemaUpdate,
        uow: UOWDep,
):
    result = await InstrumentGroupsService().update_group(
        uow=uow, group_id=group_id, update_data=update_data
    )
    return result
