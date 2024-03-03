from api.object.object_schemas import ObjectCreate
from db.dals.ObjectDAL import ObjectDAL
from db.dals.UserFavouriteObjectDAL import UserFavouriteObjectDAL
from db.dals.ObjectsFileDAL import ObjectFileDAL
from typing import Union
from db.models import Object
from aws.session import MinioTool
from service.file_service import _get_file_name_by_file_id


async def _create_new_object(body: ObjectCreate, session):
    async with session.begin():
        object_dal = ObjectDAL(session)
        await object_dal.create_object(
            name=body.name,
            longitude=body.longitude,
            latitude=body.latitude,
            location="",
            description="",
            links=[""],
            type=body.type,
        )


async def _get_all_active_objects(user_id: int, session):
    async with session.begin():
        object_dal = ObjectDAL(session)
        ufo_dal = UserFavouriteObjectDAL(session)
        object_file_dal = ObjectFileDAL(session)
        active_objects = await object_dal.get_active_objects()
        active_objects_dict = []
        for obj in active_objects:
            files_ids = await object_file_dal.get_file_id_by_object_id(obj.id)
            active_objects_dict.append(
                {
                    "id": obj.id,
                    "name": obj.name,
                    "coordinates": [obj.longitude, obj.latitude],
                    "location": obj.location,
                    "description": obj.description,
                    "links": obj.links,
                    "type": obj.type,
                    "is_favourite": await _is_fav(ufo_dal, user_id, obj.id),
                    "files_base64": await _get_object_photos(files_ids, session)
                }
            )
        return active_objects_dict


async def _get_favourite_objects(user_id: int, session):
    active_objects = await _get_all_active_objects(user_id, session)
    favourite_objects = [obj for obj in active_objects if obj["is_favourite"]]
    return favourite_objects


async def _get_files_base64(object_id, session) -> list[str]:
    object_file_dal = ObjectFileDAL(session)
    files_ids = await object_file_dal.get_file_id_by_object_id(object_id)
    objects_photos = await _get_object_photos(files_ids, session)
    return objects_photos


# get_mark_status_by_object_id_for_current_user dynamic usage???
async def _is_fav(ufo_dal, user_id: int, object_id: int) -> bool:
    result = await ufo_dal.get_mark_status_by_object_id_for_current_user(user_id, object_id)
    if result is None:
        return False
    return result


async def _get_object_photos(files_ids, session) -> list[str]:
    minio = MinioTool()
    file_base64_list = []
    for file_id in files_ids:
        file_name = await _get_file_name_by_file_id(file_id, session)
        file_base64 = await minio.download_file(file_id=file_id, file_name=file_name)
        file_base64_list.append(file_base64)
    return file_base64_list


async def _update_object(updated_object_params: dict, object_id: int, session) -> Union[int, None]:
    async with session.begin():
        object_dal = ObjectDAL(session)
        updated_object_id = await object_dal.update_object(
            object_id=object_id, **updated_object_params
        )
        return updated_object_id


async def _get_object_by_id(object_id: int, session) -> Union[Object, None]:
    async with session.begin():
        object_dal = ObjectDAL(session)
        object = await object_dal.get_object_by_id(
            object_id=object_id
        )
        if object is not None:
            return object
