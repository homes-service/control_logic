import uuid
from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def edit_one():
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all_by_user_id(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_all_by(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, id: uuid.UUID, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(
            self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self, **filter_by):
        stmt = select(self.model)
        if filter_by:
            stmt = stmt.filter_by(
                **filter_by)
        res = await self.session.execute(stmt)
        return [row[0] for row in res.all()]

    async def find_one(self, **filter_by):
        stmt = select(self.model)
        if filter_by:
            stmt = stmt.filter_by(
                **filter_by)
        res = await self.session.execute(stmt)
        try:
            res = res.scalar_one()
        except NoResultFound:
            return None
        return res
