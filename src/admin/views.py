from sqladmin import ModelView
from src.db.models import User, File, UserFile, Object, UserFavouriteObject, ObjectFile, Routes, RoutesObjects, UserFavouriteRoutes

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

class FileAdmin(ModelView, model=File):
    column_list = [File.id, File.name]
    name = "Файл"
    name_plural = "Файлы"


class UserFileAdmin(ModelView, model=UserFile):
    column_list = [UserFile.id, UserFile.user_id, UserFile.file_id]
    name = "Файл пользователя"
    name_plural = "Файлы пользователей"


class ObjectAdmin(ModelView, model=Object):
    column_list = [Object.id, Object.name]
    name = "Достопримечательность/Локация"
    name_plural = "Достопримечательности/Локации"


class UserFavouriteObjectAdmin(ModelView, model=UserFavouriteObject):
    column_list = [UserFavouriteObject.id, UserFavouriteObject.user_id, UserFavouriteObject.object_id]
    name = "Избранная достопримечательность пользователя"
    name_plural = "Избранные достопримечательности пользователей"


class ObjectFileAdmin(ModelView, model=ObjectFile):
    column_list = [ObjectFile.id, ObjectFile.object_id, ObjectFile.file_id]
    name = "Файл достопримечательности"
    name_plural = "Файлы достопримечательностей"


class RoutesAdmin(ModelView, model=Routes):
    column_list = [Routes.id, Routes.name]
    name = "Маршрут"
    name_plural = "Маршруты"


class RoutesObjectsAdmin(ModelView, model=RoutesObjects):
    column_list = [RoutesObjects.id, RoutesObjects.route_id, RoutesObjects.object_id]
    name = "Объекты маршрута"
    name_plural = "Объекты маршрутов"


class UserFavouriteRoutesAdmin(ModelView, model=UserFavouriteRoutes):
    column_list = [UserFavouriteRoutes.id, UserFavouriteRoutes.user_id, UserFavouriteRoutes.route_id]
    name = "Избранный маршрут пользователя"
    name_plural = "Избранные маршруты пользователей"