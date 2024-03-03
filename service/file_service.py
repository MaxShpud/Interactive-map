from db.dals.FileDAL import FileDal
from db.dals.UserFileDAL import UserFileDal
from db.dals.ObjectsFileDAL import ObjectFileDAL
from api.file.file_schemas import ShowFile


async def _upload_new_file(file, session) -> ShowFile:
    async with session.begin():
        file_dal = FileDal(session)
        new_file = await file_dal.upload_file(name=file.filename)
        return ShowFile(
            id=new_file.id,
            name=new_file.name
        )


async def _link_users_files(user_id, file_id, session):
    async with session.begin():
        user_file_dal = UserFileDal(session)
        await user_file_dal.is_avatar_active(user_id=user_id)
        await user_file_dal.link(user_id=user_id, file_id=file_id)


async def _link_object_files(object_id, file_id, session):
    async with session.begin():
        object_file_dal = ObjectFileDAL(session)
        await object_file_dal.link(object_id=object_id, file_id=file_id)


async def _get_file_id_by_user_id(user_id, session) -> int:
    async with session.begin():
        user_file_dal = UserFileDal(session)
        file_id = await user_file_dal.get_file_id_by_user_id(
            user_id=user_id
        )
        if file_id is not None:
            return file_id


async def _get_file_name_by_file_id(file_id, session):

    file_dal = FileDal(session)
    file_name = await file_dal.get_file_name_by_id(
        file_id=file_id
    )
    if file_name is not None:
        return file_name


async def _delete_file(user_id, session):
    async with session.begin():
        user_file_dal = UserFileDal(session)
        await user_file_dal.delete_avatar(
            user_id=user_id
        )
