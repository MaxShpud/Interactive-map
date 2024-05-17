from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger
from sqlalchemy.exc import IntegrityError
from src.service.object_service import _get_files_base64
from fastapi.responses import JSONResponse

from src.db.models import User
from src.auth.actions.auth import get_current_user_from_token
from src.service.object_service import _create_new_object
from src.service.object_service import _search_object
from src.service.object_service import _get_all_active_objects
from src.service.object_service import _get_object_by_id
from src.service.object_service import _get_favourite_objects
from src.service.UFO_service import _update_mark
from src.api.object.object_schemas import ObjectCreate
from src.api.object.object_schemas import ObjectInfoResponse
from src.api.object.object_schemas import ObjectInfo
from src.api.object.object_schemas import UpdateObjectRequest
from src.db.session import get_db

logger = getLogger(__name__)

object_router = APIRouter()


@object_router.post("")
async def create_object(body: ObjectCreate,
                        db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user_from_token)):
    if current_user.role[0] == "USER":
        raise HTTPException(status_code=403, detail="User don't have permission")
    await _create_new_object(body, db, None, True)


@object_router.get("", response_model=ObjectInfoResponse)
async def get_objects_short_info(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> ObjectInfoResponse:
    active_objects = await _get_all_active_objects(current_user.id, db)
    return ObjectInfoResponse(objects=active_objects)


@object_router.get("/favourite", response_model=ObjectInfoResponse)
async def get_favourite_objects(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> ObjectInfoResponse:
    favourite_objects = await _get_favourite_objects(current_user.id, db)
    return ObjectInfoResponse(objects=favourite_objects)


@object_router.patch("")
async def update_object(
        object_id: int,
        body: UpdateObjectRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    # if current_user.role[0] == "USER":
    #     raise HTTPException(status_code=403, detail="User don't have permission")
    updated_user_params = body.dict(exclude_unset=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for object update into should be provided.",
        )
    try:
        mark = await _update_mark(
            updated_object_params=updated_user_params,
            user_id=current_user.id,
            object_id=object_id,
            session=db
        )
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {error}"
        )
    object = await _get_object_by_id(object_id, db)
    if object is None:
        raise HTTPException(
            status_code=404,
            detail="Object not found."
        )
    files_base64 = await _get_files_base64(object.id, db)

    return ObjectInfo(
        id=object.id,
        name=object.name,
        coordinates=[object.longitude, object.latitude],
        location=object.location,
        description=object.description,
        links=object.links,
        type=object.type,
        is_favourite=mark,
        files_base64=files_base64
    )

@object_router.get("/{search}")
async def get_list_of_matches_objects_by_name(search: str,
                                              db: AsyncSession = Depends(get_db),
                                              current_user: User = Depends(get_current_user_from_token)
                                              ):
    active_objects = await _search_object(search, db)
    return JSONResponse(content=active_objects, status_code=200)