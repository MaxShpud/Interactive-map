from typing import Union
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import UserFavouriteObject


class UserFavouriteObjectDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_new_mark(self,
                              user_id: int,
                              object_id: int
                              ) -> UserFavouriteObject:
        new_mark = UserFavouriteObject(
            user_id=user_id,
            object_id=object_id
        )
        self.db_session.add(new_mark)
        await self.db_session.flush()
        return new_mark

    async def get_active_marks_for_user(self,
                                        user_id: int,
                                        ) -> list[UserFavouriteObject]:
        query = select(UserFavouriteObject).where(
            and_(UserFavouriteObject.user_id == user_id, UserFavouriteObject.is_favourite == True))
        result = await self.db_session.execute(query)
        active_marks = result.scalars().all()
        return active_marks

    async def get_mark_status_by_object_id_for_current_user(self,
                                                            user_id: int,
                                                            object_id: int) -> Union[bool, None]:
        query = select(UserFavouriteObject.is_favourite).where(
            and_(UserFavouriteObject.user_id == user_id, UserFavouriteObject.object_id == object_id))
        result = await self.db_session.execute(query)
        mark_status = result.fetchone()
        if mark_status is not None:
            return mark_status[0]

    async def update_mark(self,
                          user_id: int,
                          object_id: int,
                          **kwargs
                          ) -> bool:
        query = (
            update(UserFavouriteObject)
            .where(and_(UserFavouriteObject.user_id == user_id, UserFavouriteObject.object_id == object_id))
            .values(**kwargs)
            .returning(UserFavouriteObject.is_favourite)
        )
        result = await self.db_session.execute(query)
        mark_row = result.fetchone()
        if mark_row is not None:
            return mark_row[0]
