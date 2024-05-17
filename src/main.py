from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter

from src.api.user.user_handlers import user_router
from src.auth.login_handler import login_router
from src.api.handlers import app_router
from src.api.file.file_handlers import file_router
from src.api.object.object_handlers import object_router
from src.api.routes.routes_handlers import routes_router
from src.db.session import engine
from sqladmin import Admin, ModelView
from src.admin.views import (UserAdmin,
                             ObjectAdmin,
                             RoutesAdmin,
                             RoutesObjectsAdmin,
                            FileAdmin, ObjectFileAdmin, UserFileAdmin, UserFavouriteRoutesAdmin, UserFavouriteObjectAdmin,
                             )

app = FastAPI(title="interactive map")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/api/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/api/login", tags=["login"])
main_api_router.include_router(app_router, prefix="/api", tags=["init"])
main_api_router.include_router(file_router, prefix="/api/file", tags=["file"])
main_api_router.include_router(object_router, prefix="/api/object", tags=["object"])
main_api_router.include_router(routes_router, prefix="/api/route", tags=["routes"])
app.include_router(main_api_router)

admin = Admin(app, engine)




admin.add_view(UserAdmin)
admin.add_view(ObjectAdmin)
admin.add_view(RoutesAdmin)
admin.add_view(RoutesObjectsAdmin)
admin.add_view(FileAdmin)
admin.add_view(ObjectFileAdmin)
admin.add_view(UserFileAdmin)
admin.add_view(UserFavouriteRoutesAdmin)
admin.add_view(UserFavouriteObjectAdmin)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
