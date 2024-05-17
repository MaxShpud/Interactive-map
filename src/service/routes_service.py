from src.api.object.object_schemas import ObjectCreate
from src.api.routes.routes_schemas import RouteCreate
from src.db.dals.ObjectDAL import ObjectDAL
from src.db.dals.RoutesDAL import RoutesDAL
from src.db.dals.RoutesObjectsDAL import RoutesObjectsDAL
from src.db.dals.UserFavouriteRouteDAL import UserFavouriteRoutesDAL
from src.db.dals.UserFavouriteObjectDAL import UserFavouriteObjectDAL
from src.db.dals.ObjectsFileDAL import ObjectFileDAL
from typing import Union
from src.db.models import Object
from src.aws.session import MinioTool
from src.service.file_service import _get_file_name_by_file_id
from src.api.routes.routes_schemas import RouteInfo
from src.api.object.object_schemas import RouteObjects
from src.service.object_service import _create_new_object


async def _create_new_route(body,user_id, session):
    async with session.begin():
        route_dal = RoutesDAL(session)
        return await route_dal.create_route(
            name=body.name,
            length=body.length,
            location=body.location,
            description=body.description,
            type=body.type,
            system=body.system,
            user_id=user_id
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


async def _get_active_user_routes(user_id, session):
    async with session.begin():
        routes_dal = RoutesDAL(session)
        routes_objects_dal = RoutesObjectsDAL(session)
        object_dal = ObjectDAL(session)
        active_routes = await routes_dal.get_active_user_routes(user_id)
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


async def _create_location_with_objects(body, user_id, session):
    new_route = await _create_new_route(body.route,user_id, session)
    for element in body.objects:
        new_object = await _create_new_object(element, session, False)
        await _add_object_to_route(new_route.id, new_object.id, session)


async def _get_favourite_routes(user_id: int, session):
    active_objects = await _get_all_active_routes(user_id, session)
    favourite_objects = [obj for obj in active_objects if obj["is_favourite"]]
    return favourite_objects


async def _is_fav(ufr_dal, user_id: int, object_id: int) -> bool:
    result = await ufr_dal.get_mark_status_by_object_id_for_current_user(user_id, object_id)
    if result is None:
        return False
    return result


async def _get_all_active_routes(user_id: int, session):
    async with session.begin():
        routes_dal = RoutesDAL(session)
        ufr_dal = UserFavouriteRoutesDAL(session)
        active_routes = await routes_dal.get_active_routes()
        active_routes_dict = []
        for route in active_routes:
            active_routes_dict.append(
                {
                    "id": route.id,
                    "name": route.name,
                    "length": route.length,
                    "location": route.location,
                    "description": route.description,
                    "type": route.type,
                    "is_favourite": await _is_fav(ufr_dal, user_id, route.id)
                }
            )

        return active_routes_dict
