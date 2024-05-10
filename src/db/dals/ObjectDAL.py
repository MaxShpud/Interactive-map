from typing import Union
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Object, ObjectType


class ObjectDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_object(
            self,
            name: str,
            longitude: float,
            latitude: float,
            location: str,
            description: str,
            links: list[str],
            type: ObjectType,
            system: bool
    ) -> Object:
        new_object = Object(
            name=name,
            longitude=longitude,
            latitude=latitude,
            location=location,
            description=description,
            links=links,
            type=type,
            system=system
        )

        self.db_session.add(new_object)
        await self.db_session.flush()
        return new_object

    async def get_active_objects(self) -> list[Object]:
        query = select(Object).where(and_(Object.is_active == True, Object.system == True))
        result = await self.db_session.execute(query)
        active_objects = result.scalars().all()
        return active_objects

    async def get_object_by_id(self, object_id: int) -> Object:
        query = select(Object).where(Object.id == object_id)
        result = await self.db_session.execute(query)
        object_row = result.fetchone()
        if object_row is not None:
            return object_row[0]

    async def update_object(self, object_id: int, **kwargs) -> Union[int, None]:
        query = (
            update(Object)
            .where(and_(Object.id == object_id, Object.is_active == True))
            .values(**kwargs)
            .returning(Object.id)
        )
        result = await self.db_session.execute(query)
        update_object_id_row = result.fetchone()
        if update_object_id_row is not None:
            return update_object_id_row[0]

    async def search_objects(self, search: str) -> list[Object]:
        query = (
            select(Object.name)
            .filter(func.lower(Object.name).like(f'%{search}%'))
        )
        result = await self.db_session.execute(query)
        search_result = result.scalars().all()
        if not search_result:
            return []
        return search_result
