from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger
from sqlalchemy.exc import IntegrityError

from api.file.file_schemas import UploadedFileResponse
from db.models import User
from auth.actions.auth import get_current_user_from_token
from service.object_service import _create_new_object
from service.object_service import _get_all_active_objects
from api.object.object_schemas import ObjectCreate
from api.object.object_schemas import ObjectsShortInfoResponse
from api.object.object_schemas import ObjectsShortInfo
from db.session import get_db
from aws.session import MinioTool

logger = getLogger(__name__)

object_router = APIRouter()


@object_router.post("")
async def create_object(body: ObjectCreate,
                        db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user_from_token)):
    if current_user.role[0] == "USER":
        raise HTTPException(status_code=403, detail="User don't have permission")
    await _create_new_object(body, db)


@object_router.get("", response_model=ObjectsShortInfoResponse)
async def get_objects_short_info(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    active_objects = await _get_all_active_objects(db)
    return ObjectsShortInfoResponse(objects=active_objects)
