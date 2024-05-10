from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import RoutesObjects


class RoutesObjectsDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def link(self, route_id: int, object_id: int):
        new_link = RoutesObjects(route_id=route_id, object_id=object_id)
        self.db_session.add(new_link)
        await self.db_session.flush()

    async def get_object_id_by_route_id(self, route_id: int):
        query = select(RoutesObjects.object_id).where(and_(RoutesObjects.route_id == route_id, RoutesObjects.is_active == True))
        result = await self.db_session.execute(query)
        object_rows = result.fetchall()
        if object_rows is not None:
            objects_ids = [row[0] for row in object_rows]
            return objects_ids