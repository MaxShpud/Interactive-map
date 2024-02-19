from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger
from sqlalchemy.exc import IntegrityError

from api.schemas import UserCreate
from api.schemas import ShowUser
from api.schemas import DeleteUserResponse
from api.schemas import UpdatedUserResponse
from api.schemas import UpdateUserRequest
from db.dals import UserDAL
from db.session import get_db
from db.models import User
from auth.actions.auth import get_current_user_from_token
from auth.actions.user import _create_new_user
from auth.actions.user import _get_user_by_id
from auth.actions.user import _update_user
from auth.actions.user import _delete_user
from auth.actions.user import check_user_permission

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {error}"
        )

@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User not found."
        )
    if user_id != current_user.id:
        if await check_user_permission(
                target_user=user_for_deletion,
                current_user=current_user,
        ):
            raise HTTPException(
                status_code=403,
                detail="Forbidden."
            )
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail="User not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: int,
        body: UpdateUserRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update into should be provided.",
        )
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    if user_id != current_user.id:
        if await check_user_permission(
            target_user=user_for_update,
            current_user=current_user,
        ):
            raise HTTPException(
                status_code=403,
                detail="Forbidden."
            )
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params,
            session=db,
            user_id=user_id
        )
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {error}"
        )
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    return user
