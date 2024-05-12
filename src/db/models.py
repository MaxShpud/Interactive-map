import uuid

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum, unique

Base = declarative_base()


@unique
class Role(str, Enum):
    ROLE_ADMIN = "ADMIN"
    ROLE_USER = "USER"


@unique
class ObjectType(str, Enum):
    ARCHITECTURE = "ARCHITECTURE"
    NATURAL_RESERVES = "NATURAL_RESERVES"
    RELIGION = "RELIGION"
    NATURE = "NATURE"
    MUSEUMS = "MUSEUMS"
    WAR_MONUMENTS = "WAR_MONUMENTS"
    CULTURAL_SITES = "CULTURAL_SITES"
    USER_OBJECT = "USER_OBJECT"

@unique
class RouteType(str, Enum):
    HIKING = "HIKING"
    CYCLING = "CYCLING"
    WATER = "WATER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
    role = Column(ARRAY(String), nullable=False)
    phone_number = Column(String, nullable=True)
    about_me = Column(String, nullable=True)

    @property
    def is_admin(self) -> bool:
        return Role.ROLE_ADMIN in self.role


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class UserFile(Base):
    __tablename__ = "users_files"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    is_active = Column(Boolean, default=True)


class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)
    links = Column(ARRAY(String), nullable=True)
    type = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    system = Column(Boolean, nullable=False, default=True)
    # is_favourite = Column(Boolean, nullable=False, default=False)


class UserFavouriteObject(Base):
    __tablename__ = "user_favourite_objects"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    object_id = Column(Integer, ForeignKey("objects.id"), nullable=False)
    is_favourite = Column(Boolean, nullable=False, default=True)


class ObjectFile(Base):
    __tablename__ = "objects_files"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    object_id = Column(Integer, ForeignKey("objects.id"), nullable=False)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    is_active = Column(Boolean, default=True)


class Routes(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    length = Column(Float, nullable=False)
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)
    type = Column(String, nullable=False)
    system = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    #user_id= Column(Integer, ForeignKey("users.id"), nullable=True)


class RoutesObjects(Base):
    __tablename__ = 'routes_objects'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    object_id = Column(Integer, ForeignKey("objects.id"), nullable=False)
    is_active = Column(Boolean, default=True)