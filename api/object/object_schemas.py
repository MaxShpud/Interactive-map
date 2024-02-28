import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import constr
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator
from api.schemas import TunedModel
from api.schemas import LETTER_MATCH_PATTERN


class ObjectCreate(BaseModel):
    name: str
    longitude: float
    latitude: float
    type: str


class ObjectsShortInfo(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float
    description: str
    links: list[str]
    type: str


class ObjectsShortInfoResponse(BaseModel):
    objects: list[ObjectsShortInfo]
