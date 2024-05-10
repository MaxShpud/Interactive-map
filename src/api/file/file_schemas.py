from pydantic import BaseModel
from src.api.schemas import TunedModel


class UploadedFileResponse(BaseModel):
    name: str


class ShowFile(TunedModel):
    id: int
    name: str


class DeleteFileResponse(BaseModel):
    deleted_file_id: int
