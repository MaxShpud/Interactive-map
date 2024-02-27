from typing import Dict, Any, Coroutine

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger
from sqlalchemy.exc import IntegrityError

from api.file_schemas import UploadedFileResponse
from db.models import User
from auth.actions.auth import get_current_user_from_token
from auth.actions.user import _get_user_by_id
from service.file_service import _upload_new_file
from service.file_service import _link_users_files
from service.file_service import _delete_file
from api.file_schemas import DeleteFileResponse
from auth.actions.user import check_user_permission
from auth.security import create_access_token
from datetime import timedelta
import settings
from db.session import get_db
from auth.schemas import Token
from aws.session import MinioTool

logger = getLogger(__name__)

file_router = APIRouter()


@file_router.post("/avatar", response_model=UploadedFileResponse)
async def upload_file(file: UploadFile = File(...) ,
                      db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user_from_token),
                      ) -> UploadedFileResponse:
    minio = MinioTool()
    try:

        new_file = await _upload_new_file(file, db)
        await minio.upload_file(file, new_file.id)
        await _link_users_files(current_user.id, new_file.id, db)
        return UploadedFileResponse(name=new_file.name)
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {error}"
        )


@file_router.delete("/avatar")
async def delete_file(db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user_from_token),
                      ):
    await _delete_file(user_id=current_user.id, session=db)
