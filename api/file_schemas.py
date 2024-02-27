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


class UploadedFileResponse(BaseModel):
    name: str


class ShowFile(TunedModel):
    id: int
    name: str

class DeleteFileResponse(BaseModel):
    deleted_file_id: int