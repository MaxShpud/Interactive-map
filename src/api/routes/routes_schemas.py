from typing import Optional

from pydantic import constr
from pydantic import BaseModel
from typing_extensions import Annotated
from typing import List
from src.api.object.object_schemas import RouteObjects, ObjectCreate


class RouteCreate(BaseModel):
    name: str
    length: float
    location: str
    description: str
    type: str
    system: bool


class RouteInfo(BaseModel):
    name: str
    length: float
    location: str
    description: str
    type: str
    system: bool
    objects: List[RouteObjects]


class GetRoutes(BaseModel):
    routes: List[RouteInfo]


class CreateRouteByUser(BaseModel):
    route: RouteCreate
    objects: List[ObjectCreate]


class UpdateRouteRequest(BaseModel):
    name: Optional[str]
    length: Optional[float]
    location: Optional[str]
    description: Optional[str]
    type: Optional[str]
    system: Optional[bool]
    is_active: Optional[bool]
    is_favourite: Optional[bool]

class RouteInfo2(BaseModel):
    name: str
    length: float
    location: str
    description: str
    type: str
    system: bool
    objects: List[RouteObjects]
    is_favourite: bool

class RoutesInfoResponse(BaseModel):
    routes: List[RouteInfo2]