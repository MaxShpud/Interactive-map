import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import constr
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True  # параметр говорит пайдентику конвертировать даже не non dict объекты в json


class ShowUser(TunedModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    phone_number: str
    about_me: str


class CurrentUserInfo(TunedModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    phone_number: str
    about_me: str
    photo_id: int
    photo_base64: str


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: int


class UpdatedUserResponse(BaseModel):
    updated_user_id: int


class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    phone_number: Optional[constr(min_length=0)]
    about_me: Optional[constr(min_length=0)]

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value
