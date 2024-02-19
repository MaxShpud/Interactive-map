import uuid

from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum, unique

Base = declarative_base()


@unique
class Role(str, Enum):
    ROLE_ADMIN = "ADMIN"
    ROLE_USER = "USER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
    role = Column(ARRAY(String), nullable=False)

    @property
    def is_admin(self) -> bool:
        return Role.ROLE_ADMIN in self.role
