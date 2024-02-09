from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UserCreate, ShowUser, DeleteUserResponse
from db.dals import UserDAL
from db.session import get_db
from auth.actions.user import _create_new_user

from typing import Union
from uuid import UUID

user_router = APIRouter()




async def _delete_user(user_uuid, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user(
                user_uuid=user_uuid,
            )
            return deleted_user_id


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)

@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_uuid:UUID, db: AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(user_uuid, db)
    if deleted_user_id in None:
        raise HTTPException(status_code=404, detail=f"User with id {user_uuid} not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)

