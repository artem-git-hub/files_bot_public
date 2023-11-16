from typing import Union

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class DebugMes(BaseMiddleware):
    skip_patterns = ["debug"]

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    async def on_post_process_message(self, obj: Union[types.Message, types.CallbackQuery], data_from_filters: list,
                                      data: dict):
        # print(obj.text)
        pass
