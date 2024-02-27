from typing import Union
from uuid import UUID
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Role, File, UserFile


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self,
            name: str,
            surname: str,
            email: str,
            hashed_password: str,
            role: list[Role],
            phone_number: str,
            about_me: str
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password,
            role=role,
            phone_number="",
            about_me=""
        )

        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        result = await self.db_session.execute(query)
        user_row = result.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_id(self, user_id: int) -> Union[User, None]:
        query = select(User).where(User.id == user_id)
        result = await self.db_session.execute(query)
        user_row = result.fetchone()
        if user_row is not None:
            return user_row[0]

    async def delete_user(self, user_id: int) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.id)
        )
        result = await self.db_session.execute(query)
        deleted_user_id_row = result.fetchone()
        if deleted_user_id_row is not None:
            return int(deleted_user_id_row[0])

    async def update_user(self, user_id: int, **kwargs) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.id)
        )
        result = await self.db_session.execute(query)
        update_user_id_row = result.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]


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
        query=(
            update(File)
            .where(and_(File.id == file_id, File.is_active == True))
            .values(is_active=False)
            .returning(File.id)
        )
        result = await self.db_session.execute(query)
        deleted_file_id_row = result.fetchone()
        if deleted_file_id_row is not None:
            return int(deleted_file_id_row[0])


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
