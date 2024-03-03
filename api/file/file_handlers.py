from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger
from sqlalchemy.exc import IntegrityError

from api.file.file_schemas import UploadedFileResponse
from db.models import User
from auth.actions.auth import get_current_user_from_token
from service.file_service import _upload_new_file
from service.file_service import _link_users_files
from service.file_service import _delete_file
from service.file_service import _link_object_files
from db.session import get_db
from aws.session import MinioTool
from db.dals.ObjectsFileDAL import ObjectFileDAL

logger = getLogger(__name__)

file_router = APIRouter()


@file_router.post("/avatar", response_model=UploadedFileResponse)
async def upload_avatar(file: UploadFile = File(...),
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
async def delete_avatar(db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user_from_token),
                        ):
    await _delete_file(user_id=current_user.id, session=db)


@file_router.post("/object", response_model=UploadedFileResponse)
async def upload_object(object_id: int,
                        file: UploadFile = File(...),
                        db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user_from_token),
                        ) -> UploadedFileResponse:
    minio = MinioTool()
    try:
        if current_user.role[0] == "USER":
            raise HTTPException(status_code=403, detail="User don't have permission")
        new_file = await _upload_new_file(file, db)
        await minio.upload_file(file, new_file.id)
        await _link_object_files(object_id, new_file.id, db)
        return UploadedFileResponse(name=new_file.name)
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {error}"
        )


@file_router.get("/test")
async def test(object_id: int,
               db: AsyncSession = Depends(get_db),
               ):
    test = ObjectFileDAL(db)
    result = await test.get_file_id_by_object_id(object_id)
    return {"response": result}