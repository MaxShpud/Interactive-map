from api.object.object_schemas import ObjectCreate
from db.dals.ObjectDAL import ObjectDAL
from db.dals.UserFavouriteObjectDAL import UserFavouriteObjectDAL
from typing import Union
from db.models import Object


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
        active_objects = await object_dal.get_active_objects()

        active_objects_dict = [
            {
                "id": obj.id,
                "name": obj.name,
                "coordinates": [obj.longitude, obj.latitude],
                # "longitude": obj.longitude,
                # "latitude": obj.latitude,
                "location": obj.location,
                "description": obj.description,
                "links": obj.links,
                "type": obj.type,
                "is_favourite": await __is_fav(ufo_dal, user_id, obj.id)
            }
            for obj in active_objects
        ]
        return active_objects_dict


#get_mark_status_by_object_id_for_current_user dynamic usage???
async def __is_fav(ufo_dal, user_id: int, object_id: int) -> bool:
    result = await ufo_dal.get_mark_status_by_object_id_for_current_user(user_id, object_id)
    if result is None:
        return False
    return result


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
