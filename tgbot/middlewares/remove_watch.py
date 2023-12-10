from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class RemoveWatch(BaseMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    async def on_pre_process_update(self, obj: types.Update, data: dict):
        if obj.callback_query:
            await obj.callback_query.answer()
