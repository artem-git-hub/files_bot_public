from typing import Union

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from pyparsing import dbl_slash_comment

from tgbot.db import db_com_user
from tgbot.db.db_com_user import select_user, add_user
from tgbot.db.models.user import User


class UpdateUserData(BaseMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, **kwargs):
        super(UpdateUserData, self).__init__()
        self.kwargs = kwargs

    async def on_pre_process_message(self, obj: types.Message, data: dict):
        tg_user = obj.from_user
        user: User = await select_user(id=tg_user.id)
        if user is None:
            await add_user(id=tg_user.id, username=tg_user.username, fullname=tg_user.full_name)

    async def on_pre_process_callback_query(self, obj: types.CallbackQuery, data: dict):
        tg_user = obj["from"]
        user: User = await select_user(id=tg_user.id)
        if user is None:
            await add_user(id=tg_user.id, username=tg_user.username, fullname=tg_user.full_name)

    async def on_post_process_message(self, obj: Union[types.Message, types.CallbackQuery], data_from_filters: list,
                                      data: dict):
        if type(obj) in [types.Message, types.CallbackQuery]:
            if type(obj) == types.CallbackQuery:
                message = obj.message
                user_id = obj.message.from_user.id
            else:
                message = obj
                user_id = obj.from_user.id
            try:
                db_user = await select_user(id=user_id)
                if db_user.username != message.from_user.username:
                    await db_com_user.update_user_data(id=message.from_user.id,
                                                       username=message.from_user.username if message.from_user.username is not None else "")
                if db_user.fullname != message.from_user.full_name:
                    await db_com_user.update_user_data(id=message.from_user.id,
                                                       fullname=message.from_user.full_name)
            except AttributeError as e:
                print(e)
                await message.answer("Нажми /start")
