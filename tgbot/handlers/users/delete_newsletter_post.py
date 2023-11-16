from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.callback_data import for_key_channels


async def del_newsletter_post(call: types.CallbackQuery):
    await call.message.delete()


def register_del_newsletter_post_handler(dp: Dispatcher):
    dp.register_callback_query_handler(del_newsletter_post, for_key_channels.filter(command="delete_newsletter_post"))
