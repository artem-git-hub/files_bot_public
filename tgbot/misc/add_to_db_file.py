from random import choice
from uuid import uuid4

from aiogram import types

from tgbot.db import db_com_file
from tgbot.db.models.file import File
from tgbot.db.models.user import User
from tgbot.misc.gen_file_id import gen_file_id
from tgbot.misc.gen_name_file import gen_name_file
from tgbot.misc.get_data_file import get_data_file


async def add_to_db_file(message: types.Message):
    user = await User.get(message.from_user.id)
    tg_id = ""
    user_id = ""
    filename = ""
    file_type = ""
    description = ""
    long_id = user.long_id

    if long_id:
        id = str()
        begin = str(uuid4()) + str(uuid4()) + str(uuid4())
        for i in range(64):
            id += begin[i]
    else:
        id = await gen_file_id()
        file = await File.query.where(File.id == id).gino.all()
        while file:
            id = await gen_file_id()
            if not await File.query.where(File.id == id).gino.all():
                break

        # print(file)

    user_id = message.from_user.id
    description = message.caption if message.caption is not None else ""
    tg_id, filename, file_type = await get_data_file(message=message, get_filename=True)

    await db_com_file.add_file(id=id, tg_id=tg_id, user_id=user_id, type=file_type, filename=filename,
                               description=description)

    file = {
        "id": id,
        "tg_id": tg_id,
        "user_id": user_id,
        "type": file_type,
        "filename": filename,
        "description": description
    }
    return file
