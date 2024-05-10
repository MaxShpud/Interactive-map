from typing import Optional

from pydantic import constr
from pydantic import BaseModel
from typing_extensions import Annotated
from typing import List


class ObjectCreate(BaseModel):
    name: str
    longitude: float
    latitude: float
    type: str


class Coordinates(BaseModel):
    longitude: float
    latitude: float


class ObjectInfo(BaseModel):
    id: int
    name: str
    coordinates: List[Annotated[float, float]]
    location: str
    description: str
    links: List[str]
    type: str
    is_favourite: bool
    files_base64: List[str]


class ObjectInfoResponse(BaseModel):
    objects: List[ObjectInfo]


class UpdateObjectRequest(BaseModel):
    name: Optional[constr(min_length=0)]
    longitude: Optional[float]
    latitude: Optional[float]
    location: Optional[constr(min_length=0)]
    description: Optional[constr(min_length=0)]
    links: Optional[List[str]]
    type: Optional[constr(min_length=0)]
    is_active: Optional[bool]
    is_favourite: Optional[bool]

class RouteObjects(BaseModel):
    name: str
    coordinates: List[Annotated[float, float]]
    location: str
    description: str
    type: str


