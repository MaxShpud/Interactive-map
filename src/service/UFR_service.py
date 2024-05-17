"""
SERVICE FOR UserFavouriteObject
"""

from src.db.dals.UserFavouriteRouteDAL import UserFavouriteRoutesDAL


async def _update_mark(updated_object_params: dict, user_id: int, route_id: int, session) -> bool:
    async with session.begin():
        uso_dal = UserFavouriteRoutesDAL(session)
        is_uso = await uso_dal.get_mark_status_by_object_id_for_current_user(
            user_id, route_id
        )
        if is_uso is None:
            await uso_dal.create_new_mark(user_id, route_id)
            mark = True
        else:
            mark = await uso_dal.update_mark(user_id, route_id, **updated_object_params)
        return mark
