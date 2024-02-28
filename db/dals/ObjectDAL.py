from typing import Union
from uuid import UUID
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Object, ObjectType


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
            type: ObjectType
    ) -> Object:
        new_object = Object(
            name=name,
            longitude=longitude,
            latitude=latitude,
            location=location,
            description=description,
            links=links,
            type=type
        )

        self.db_session.add(new_object)
        await self.db_session.flush()
        return new_object

    async def get_active_objects(self) -> list[Object]:
        query = select(Object).where(Object.is_active == True)
        result = await self.db_session.execute(query)
        active_objects = result.scalars().all()
        return active_objects
