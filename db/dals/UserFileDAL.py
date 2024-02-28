from typing import Union
from uuid import UUID
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import UserFile


class UserFileDal:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def link(self, user_id: int, file_id: int):
        new_link = UserFile(user_id=user_id, file_id=file_id)
        self.db_session.add(new_link)
        await self.db_session.flush()

    async def is_avatar_active(self, user_id: int):
        query = (
            update(UserFile)
            .where(and_(UserFile.user_id == user_id, UserFile.is_active == True))
            .values(is_active=False)
            .returning(UserFile.id)
        )
        await self.db_session.execute(query)

    async def get_file_id_by_user_id(self, user_id) -> int:
        query = select(UserFile.file_id).where(and_(UserFile.user_id == user_id, UserFile.is_active == True))
        result = await self.db_session.execute(query)
        user_row = result.fetchone()
        if user_row is not None:
            return user_row[0]

    async def delete_avatar(self, user_id: int):
        deletion_query = (
            update(UserFile)
            .where(and_(UserFile.user_id == user_id, UserFile.is_active == True))
            .values(is_active=False)
            .returning(UserFile.id)
        )
        await self.db_session.execute(deletion_query)
        set_active_query = (
            update(UserFile)
            .where(and_(UserFile.user_id == user_id, UserFile.file_id == 1, UserFile.is_active == False))
            .values(is_active=True)
            .returning(UserFile.id)
        )
        await self.db_session.execute(set_active_query)
