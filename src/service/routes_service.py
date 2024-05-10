from src.api.object.object_schemas import ObjectCreate
from src.api.routes.routes_schemas import RouteCreate
from src.db.dals.ObjectDAL import ObjectDAL
from src.db.dals.RoutesDAL import RoutesDAL
from src.db.dals.RoutesObjectsDAL import RoutesObjectsDAL
from src.db.dals.UserFavouriteObjectDAL import UserFavouriteObjectDAL
from src.db.dals.ObjectsFileDAL import ObjectFileDAL
from typing import Union
from src.db.models import Object
from src.aws.session import MinioTool
from src.service.file_service import _get_file_name_by_file_id
from src.api.routes.routes_schemas import RouteInfo
from src.api.object.object_schemas import RouteObjects
from src.service.object_service import _create_new_object


async def _create_new_route(body, session):
    async with session.begin():
        route_dal = RoutesDAL(session)
        return await route_dal.create_route(
            name=body.name,
            length=body.length,
            location=body.location,
            description=body.description,
            type=body.type,
            system=body.system,
        )




async def _add_object_to_route(
        route_id, object_id, session
):
    async with session.begin():
        routes_objects_dal = RoutesObjectsDAL(session)
        await routes_objects_dal.link(route_id, object_id)


async def _get_route_objects(route_id, session) -> RouteInfo:
    async with session.begin():
        routes_objects_dal = RoutesObjectsDAL(session)
        routes_dal = RoutesDAL(session)
        route = await routes_dal.get_route_by_id(route_id)
        object_dal = ObjectDAL(session)
        objects_ids = await routes_objects_dal.get_object_id_by_route_id(route_id)
        objects = []
        for object_id in objects_ids:
            obj = await object_dal.get_object_by_id(object_id)
            objects.append(RouteObjects(
                name=obj.name,
                coordinates=[obj.longitude, obj.latitude],
                location=obj.location,
                description=obj.description,
                type=obj.type,
            ))
        return RouteInfo(
            name=route.name,
            length=route.length,
            location=route.location,
            description=route.description,
            type=route.type,
            system=route.system,
            objects=objects
        )


async def _get_active_system_routes(session):
    async with session.begin():
        routes_dal = RoutesDAL(session)
        routes_objects_dal = RoutesObjectsDAL(session)
        object_dal = ObjectDAL(session)
        active_routes = await routes_dal.get_active_routes()
        routes = []
        for route in active_routes:
            objects_ids = await routes_objects_dal.get_object_id_by_route_id(route.id)
            objects = []
            for object_id in objects_ids:
                obj = await object_dal.get_object_by_id(object_id)
                objects.append(RouteObjects(
                    name=obj.name,
                    coordinates=[obj.longitude, obj.latitude],
                    location=obj.location,
                    description=obj.description,
                    type=obj.type,
                ))
            routes.append(RouteInfo(
                name=route.name,
                length=route.length,
                location=route.location,
                description=route.description,
                type=route.type,
                system=route.system,
                objects=objects
            ))
        return routes

async def _create_location_with_objects(body, session):
    new_route = await _create_new_route(body.route, session)
    for element in body.objects:
        new_object = await _create_new_object(element, session, False)
        await _add_object_to_route(new_route.id, new_object.id, session)