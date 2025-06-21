import uuid

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from schemas.instrument_groups import InstrumentGroupsSchemaAdd, \
    InstrumentGroupsSchemaAddResponse, InstrumentGroupsSchema, \
    InstrumentGroupSchemaUpdate
from utils.unitofwork import IUnitOfWork


class InstrumentGroupsService:
    async def add_group(
            self,
            uow: IUnitOfWork,
            instrument_group: InstrumentGroupsSchemaAdd
    ):
        group_dict = instrument_group.model_dump()
        async with uow:
            group_id = await uow.instrument_group.add_one(group_dict)
            await uow.commit()
        return group_id

    async def get_groups(self, uow: IUnitOfWork, account_id: uuid.UUID):
        async with uow:
            groups = await uow.instrument_group.find_all(
                account_id=account_id
            )
            result = [InstrumentGroupsSchema.model_validate(group) 
                      for group in groups]
            return result
    
    async def get_group_by_id(self, uow: IUnitOfWork, group_id: uuid.UUID):
        async with uow:
            try:
                group = await uow.instrument_group.find_one(
                    id=group_id
                )
            except NoResultFound:
                return None
            result = InstrumentGroupsSchema.model_validate(group)
            return result

    async def update_group(self,
                          uow: IUnitOfWork,
                          update_data: InstrumentGroupSchemaUpdate,
                          group_id: uuid.UUID):
        async with uow:
            group = await uow.instrument_group.find_one(id=group_id)
            if not group:
                raise HTTPException(status_code=404, detail="Group not found")

            update_dict = update_data.dict(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(group, key, value)

            await uow.commit()
            return InstrumentGroupsSchema.model_validate(group)

        
