from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger
from sqlalchemy.exc import IntegrityError

from src.api.user.user_schemas import UserCreate
from src.api.user.user_schemas import ShowUser
from src.api.user.user_schemas import DeleteUserResponse
from src.api.user.user_schemas import UpdateUserRequest
from src.api.user.user_schemas import CurrentUserInfo
from src.db.session import get_db
from src.db.models import User
from src.auth.actions.auth import get_current_user_from_token
from src.auth.actions.user import _create_new_user
from src.auth.actions.user import _get_user_by_id
from src.auth.actions.user import _update_user
from src.auth.actions.user import _get_current_user_info
from src.auth.actions.user import _delete_user
from src.auth.actions.user import check_user_permission
from src.auth.security import create_access_token
from datetime import timedelta
from src import config
from src.auth.schemas import Token

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/create")
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> Token:
    try:
        user = await _create_new_user(body, db)
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {error}"
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer", role="USER")


@user_router.delete("", response_model=DeleteUserResponse)
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


@user_router.patch("", response_model=CurrentUserInfo)
async def update_user_by_id(
        user_id: int,
        body: UpdateUserRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> CurrentUserInfo:
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
        await _update_user(
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
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    return await _get_current_user_info(user, db)

    #return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.get("", response_model=ShowUser)
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


@user_router.get("/me", response_model=ShowUser)
async def get_current_user(
        user: User = Depends(get_current_user_from_token)
):
    return user

@user_router.get("/current", response_model=CurrentUserInfo)
async def get_current_user(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user_from_token)
):
    return await _get_current_user_info(user, db)
