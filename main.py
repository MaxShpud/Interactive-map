from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter

from api.user_handlers import user_router
from auth.login_handler import login_router
from api.handlers import app_router
from api.file_handlers import file_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="interactive map")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)
main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/api/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/api/login", tags=["login"])
main_api_router.include_router(app_router, prefix="/api", tags=["init"])
main_api_router.include_router(file_router, prefix="/api/file", tags=["file"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
