from api.schemas import ShowUser
from api.schemas import UserCreate
from db.dals import UserDAL
from auth.hashing import Hasher
from typing import Union
from db.models import User, Role


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
            role=[
                Role.ROLE_USER
            ],
        )
        return ShowUser(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def _get_user_by_id(user_id, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id
        )
        if user is not None:
            return user


async def _delete_user(user_id, session) -> Union[int, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id
        )
        return deleted_user_id


async def _update_user(
        updated_user_params: dict, user_id: int, session
) -> Union[int, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id, **updated_user_params
        )
        return updated_user_id


async def check_user_permission(target_user: User, current_user: User) -> bool:
    if target_user.id != current_user.id:
        if Role.ROLE_ADMIN in current_user.role:
            return False
        if (
                Role.ROLE_ADMIN in target_user.role
                and Role.ROLE_ADMIN in current_user.role
        ):
            return False
    return True
