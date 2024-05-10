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
from src.api.routes.routes_schemas import RouteCreate, GetRoutes, CreateRouteByUser
from src.api.object.object_schemas import ObjectInfoResponse
from src.api.object.object_schemas import ObjectInfo
from src.api.object.object_schemas import UpdateObjectRequest
from src.db.session import get_db
from src.service.routes_service import _create_new_route
from src.service.routes_service import _add_object_to_route
from src.service.routes_service import _get_route_objects
from src.service.routes_service import _get_active_system_routes
from src.service.routes_service import _create_location_with_objects

logger = getLogger(__name__)

routes_router = APIRouter()


@routes_router.post("")
async def create_route(body: RouteCreate,
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user_from_token)):
    if current_user.role[0] == "USER":
        raise HTTPException(status_code=403, detail="User don't have permission")
    await _create_new_route(body, db)


@routes_router.post("/user")
async def create_route_by_user(body: CreateRouteByUser,
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user_from_token)):
    await _create_location_with_objects(body, db)

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
