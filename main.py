from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter

from api.user.user_handlers import user_router
from auth.login_handler import login_router
from api.handlers import app_router
from api.file.file_handlers import file_router
from api.object.object_handlers import object_router

app = FastAPI(title="interactive map")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/api/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/api/login", tags=["login"])
main_api_router.include_router(app_router, prefix="/api", tags=["init"])
main_api_router.include_router(file_router, prefix="/api/file", tags=["file"])
main_api_router.include_router(object_router, prefix="/api/object", tags=["object"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
