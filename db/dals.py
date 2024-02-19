from typing import Union
from uuid import UUID
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Role


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
            role: list[Role]
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password,
            role=role,
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