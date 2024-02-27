from minio import Minio
from minio.error import S3Error
import uuid
from threading import Thread, Lock
from typing import Tuple
from settings import MINIO_HOST, MINIO_PORT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME
import base64

class Singleton(type):
    _instances = {}
    _lock = Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class MinioTool(metaclass=Singleton):
    def __init__(self):
        self.client = Minio(
            endpoint=f'{MINIO_HOST}:{MINIO_PORT}',
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )

    async def __create_bucket(self):
        try:
            if not self.client.bucket_exists(MINIO_BUCKET_NAME):
                self.client.make_bucket(MINIO_BUCKET_NAME)
        except S3Error as error:
            raise error

    async def upload_file(self, file, file_id):
        try:
            await self.__create_bucket()
            file_name = f"{file_id}_{file.filename}"
            self.client.fput_object(MINIO_BUCKET_NAME, file_name, file.file.fileno())
        except S3Error as error:
            raise error

    async def download_file(self, file_id: int, file_name: str) -> str:
        try:
            await self.__create_bucket()
            self.client.fget_object(MINIO_BUCKET_NAME, f'{file_id}_{file_name}', f"aws/temp_storage/{file_id}_{file_name}")
            file_base64 = await self.__to_base64(
                f"aws/temp_storage/{file_id}_{file_name}")
            return file_base64
        except S3Error as error:
            raise error

    @staticmethod
    async def __to_base64(file_name: str) -> str:
        with open(f"{file_name}", 'rb') as binary_file:
            binary_file_data = binary_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            base64_message = base64_encoded_data.decode('utf-8')
        return base64_message
