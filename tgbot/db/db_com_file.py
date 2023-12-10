import uuid

from asyncpg import UniqueViolationError
from sqlalchemy import func

from tgbot.db.models.file import File
from tgbot.db.models.user import User
from tgbot.misc.gen_file_id import gen_file_id


async def add_file(id: str, tg_id: str, user_id: int, type: str, filename: str = "", description: str = "",
                   for_me: bool = False):
    user = await User.get(user_id)
    file = File(id=id, tg_id=tg_id, user_id=user_id, type=type, filename=filename, description=description,
                for_me=for_me)
    await file.create()


async def select_file(id: str):
    file = await File.query.where(File.id == id).gino.first()
    return file


async def count_files():
    total = await func.count(File.id).gino.scalar()
    return total


async def delete_file(id: str):
    file_stat = await File.delete.where(File.id == id).gino.status()
    return file_stat[0][-1]


async def update_file_data(id: str, user_id: int = None, filename: str = None, description: str = None,
                           new_file_id: str = None, for_me: bool = None):
    file = await File.get(id)
    if user_id:
        await file.update(user_id=user_id).apply()
    if filename:
        await file.update(filename=filename).apply()
    if description:
        await file.update(description=description).apply()
    if for_me is not None:
        await file.update(for_me=for_me).apply()

    if new_file_id:
        pass
