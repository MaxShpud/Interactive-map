from typing import Union
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import File


class FileDal:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def upload_file(self, name: str) -> File:
        new_file = File(name=name)
        self.db_session.add(new_file)
        await self.db_session.flush()
        return new_file

    async def get_file_name_by_id(self, file_id) -> str:
        query = select(File.name).where(and_(File.id == file_id, File.is_active == True))
        result = await self.db_session.execute(query)
        file_row = result.fetchone()
        if file_row is not None:
            return file_row[0]

    async def delete_file(self, file_id: int) -> Union[int, None]:
        query = (
            update(File)
            .where(and_(File.id == file_id, File.is_active == True))
            .values(is_active=False)
            .returning(File.id)
        )
        result = await self.db_session.execute(query)
        deleted_file_id_row = result.fetchone()
        if deleted_file_id_row is not None:
            return int(deleted_file_id_row[0])
