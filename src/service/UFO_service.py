"""
SERVICE FOR UserFavouriteObject
"""

from src.db.dals.UserFavouriteObjectDAL import UserFavouriteObjectDAL


async def _update_mark(updated_object_params: dict, user_id: int, object_id: int, session) -> bool:
    async with session.begin():
        uso_dal = UserFavouriteObjectDAL(session)
        is_uso = await uso_dal.get_mark_status_by_object_id_for_current_user(
            user_id, object_id
        )
        if is_uso is None:
            await uso_dal.create_new_mark(user_id, object_id)
            mark = True
        else:
            mark = await uso_dal.update_mark(user_id, object_id, **updated_object_params)
        return mark
