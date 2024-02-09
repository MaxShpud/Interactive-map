from api.schemas import ShowUser
from api.schemas import UserCreate
from db.dals import UserDAL
from auth.hashing import Hasher


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
        )
        return ShowUser(
            id=user.id,
            user_uuid=user.user_uuid,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )
