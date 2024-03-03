from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ObjectFile


class ObjectFileDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def link(self, object_id: int, file_id: int):
        new_link = ObjectFile(object_id=object_id, file_id=file_id)
        self.db_session.add(new_link)
        await self.db_session.flush()

    async def get_file_id_by_object_id(self, object_id: int):
        query = select(ObjectFile.file_id).where(and_(ObjectFile.object_id == object_id, ObjectFile.is_active == True))
        result = await self.db_session.execute(query)
        object_rows = result.fetchall()
        if object_rows is not None:
            file_ids = [row[0] for row in object_rows]
            return file_ids