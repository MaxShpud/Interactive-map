from envparse import Env

env = Env()


DB_URL = "postgresql+asyncpg://postgres:root@127.0.0.1:5432/postgres"

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=60)

# test envs
TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test",
)

MINIO_ROOT_USER = "admin"
MINIO_ROOT_PASSWORD = "admin"
MINIO_SECRET_KEY = "SpFFQb6IppbZ7B7YikEpYD84pCN93xfon5dFuouk"
MINIO_ACCESS_KEY = "AlAp3Guo4kftPutj8i0y"
MINIO_HOST = "127.0.0.1"
MINIO_PORT = "9000"
MINIO_BUCKET_NAME = "user-photos"

ORM_KEY = "5b3ce3597851110001cf62486ce3e3efab2046998cd052ead4ee2bbc"
