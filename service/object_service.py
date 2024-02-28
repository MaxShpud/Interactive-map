from api.object.object_schemas import ObjectCreate
from db.dals.ObjectDAL import ObjectDAL


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


async def _get_all_active_objects(session):
    async with session.begin():
        object_dal = ObjectDAL(session)
        active_objects = await object_dal.get_active_objects()
        active_objects_dict = [
            {
                "id": obj.id,
                "name": obj.name,
                "longitude": obj.longitude,
                "latitude": obj.latitude,
                "description": obj.description,
                "links": obj.links,
                "type": obj.type
            }
            for obj in active_objects
        ]
        return active_objects_dict
