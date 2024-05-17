from typing import Union
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Routes, RouteType


class RoutesDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_route(
            self,
            name: str,
            length: float,
            location: str,
            description: str,
            type: RouteType,
            system: bool,
            user_id: int
    ) -> Routes:
        new_route = Routes(
            name=name,
            length=length,
            location=location,
            description=description,
            type=type,
            system=system,
            user_id=user_id
        )

        self.db_session.add(new_route)
        await self.db_session.flush()
        return new_route

    async def get_active_routes(self) -> list[Routes]:
        query = select(Routes).where(and_(Routes.is_active == True, Routes.system == True))
        result = await self.db_session.execute(query)
        active_objects = result.scalars().all()
        return active_objects

    async def get_active_user_routes(self, user_id) -> list[Routes]:
        query = select(Routes).where(and_(Routes.is_active == True, Routes.system == False, Routes.user_id == user_id))
        result = await self.db_session.execute(query)
        active_objects = result.scalars().all()
        return active_objects

    async def get_route_by_id(self, route_id: int) -> Routes:
        query = select(Routes).where(Routes.id == route_id)
        result = await self.db_session.execute(query)
        route_row = result.fetchone()
        if route_row is not None:
            return route_row[0]
    #
    # async def update_object(self, object_id: int, **kwargs) -> Union[int, None]:
    #     query = (
    #         update(Object)
    #         .where(and_(Object.id == object_id, Object.is_active == True))
    #         .values(**kwargs)
    #         .returning(Object.id)
    #     )
    #     result = await self.db_session.execute(query)
    #     update_object_id_row = result.fetchone()
    #     if update_object_id_row is not None:
    #         return update_object_id_row[0]
    #
    # async def search_objects(self, search: str) -> list[Object]:
    #     query = (
    #         select(Object.name)
    #         .filter(func.lower(Object.name).like(f'%{search}%'))
    #     )
    #     result = await self.db_session.execute(query)
    #     search_result = result.scalars().all()
    #     if not search_result:
    #         return []
    #     return search_result
