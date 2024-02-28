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
    name = Column(String, nullable=False, unique=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)
    links = Column(ARRAY(String), nullable=True)
    type = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
