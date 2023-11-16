from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class OnlyUser(BaseMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    async def on_process_message(self, obj: Union[types.Message, types.CallbackQuery], data: dict):
        if obj.chat.type != "private":
            state: FSMContext = data.get("state")
            language = (await state.get_data()).get("language")
            raise CancelHandler()
