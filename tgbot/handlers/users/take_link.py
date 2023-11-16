import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from tgbot.misc.send_file import send_file
import tgbot.db.db_com_user as db_user


async def take_link(message: types.Message, state: FSMContext):

    await db_user.add_user(id=message.from_user.id,
                           username=message.from_user.username if message.from_user.username is not None else "",
                           fullname=message.from_user.full_name)
    file_id = message.get_args()
    await send_file(message=message, with_save=False, file_id=file_id, state=state)


def register_take_link(dp: Dispatcher):
    dp.register_message_handler(take_link, CommandStart(deep_link=re.compile(r'^[a-zA-Z0-9_-]{5,64}$')), state="*")
    # dp.register_message_handler(take_link, CommandStart(deep_link=re.compile(r'^[a-zA-Z0-9_-]{64}$')), state="*")
