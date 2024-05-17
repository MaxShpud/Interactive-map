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
from src.api.routes.routes_schemas import RouteCreate, RoutesInfoResponse, GetRoutes, CreateRouteByUser, UpdateRouteRequest, RouteInfo2
from src.api.object.object_schemas import ObjectInfoResponse
from src.api.object.object_schemas import ObjectInfo
from src.api.object.object_schemas import UpdateObjectRequest
from src.db.session import get_db
from src.service.routes_service import _create_new_route
from src.service.routes_service import _add_object_to_route
from src.service.routes_service import _get_route_objects
from src.service.routes_service import _get_active_system_routes
from src.service.routes_service import _create_location_with_objects
from src.service.routes_service import _get_favourite_routes
from src.service.UFR_service import _update_mark
from src.service.routes_service import _get_active_user_routes

logger = getLogger(__name__)

routes_router = APIRouter()


@routes_router.post("")
async def create_route(body: RouteCreate,
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user_from_token)):
    if current_user.role[0] == "USER":
        raise HTTPException(status_code=403, detail="User don't have permission")
    await _create_new_route(body, current_user.id, db)


@routes_router.post("/user")
async def create_route_by_user(body: CreateRouteByUser,
                               db: AsyncSession = Depends(get_db),
                               current_user: User = Depends(get_current_user_from_token)):
    await _create_location_with_objects(body, current_user.id, db)


@routes_router.post("/{route_id}/{object_id}")
async def add_object_to_route(route_id: int,
                              object_id: int,
                              db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(get_current_user_from_token)
                              ):
    if current_user.role[0] == "USER":
        raise HTTPException(status_code=403, detail="User don't have permission")
    await _add_object_to_route(route_id, object_id, db)


@routes_router.get("/{route_id}")
async def get_route_by_id(route_id: int,
                          db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user_from_token)):
    return await _get_route_objects(route_id, db)


@routes_router.get("s")
async def get_active_system_routes(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    routes = await _get_active_system_routes(db)
    return GetRoutes(routes=routes)

@routes_router.get("s/user")
async def get_active_user_routes(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    routes = await _get_active_user_routes(current_user.id, db)
    return GetRoutes(routes=routes)


@routes_router.patch("")
async def update_object(
        route_id: int,
        body: UpdateRouteRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    # if current_user.role[0] == "USER":
    #     raise HTTPException(status_code=403, detail="User don't have permission")
    updated_user_params = body.dict(exclude_unset=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for route update into should be provided.",
        )
    try:
        mark = await _update_mark(
            updated_object_params=updated_user_params,
            user_id=current_user.id,
            route_id=route_id,
            session=db
        )
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {error}"
        )
    route = await _get_route_objects(route_id, db)
    if route is None:
        raise HTTPException(
            status_code=404,
            detail="Route not found."
        )
    return RouteInfo2(
        name=route.name,
        length=route.length,
        location=route.location,
        description=route.description,
        type=route.type,
        system=route.system,
        objects=route.objects,
        is_favourite=mark
    )


@routes_router.get("s/favourite")
async def get_favourite(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    favourite_objects = await _get_favourite_routes(current_user.id, db)
    return {"routes": favourite_objects}
