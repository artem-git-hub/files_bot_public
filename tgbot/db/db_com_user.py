from asyncpg import UniqueViolationError
from sqlalchemy import func

from tgbot.db.models.user import User


async def add_user(id: int, username: str, fullname: str = "", language: str = "", long_id: bool = False):
    try:
        user = User(id=id, username=username, fullname=fullname, language=language, long_id=long_id)

        await user.create()
    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def count_users():
    total = await func.count(User.id).gino.scalar()
    return total


async def update_user_data(id: int, username: str = None, fullname: str = None, language: str = None,
                           long_id: bool = None):
    user = await User.get(id)
    if username:
        await user.update(username=username).apply()
    if fullname:
        await user.update(fullname=fullname).apply()
    if language:
        await user.update(language=language).apply()
    if long_id is not None:
        await user.update(long_id=long_id).apply()
