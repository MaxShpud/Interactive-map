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