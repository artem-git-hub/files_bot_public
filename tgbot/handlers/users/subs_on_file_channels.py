from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.callback_data import for_key_subs_on_channel
from tgbot.misc.add_channel_click import add_channels_click
from tgbot.misc.get_sub_on_file_channels import get_sub_on_file_channels
from tgbot.misc.send_file import send_file


async def im_subs(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    file = (await state.get_data()).get("file")
    is_member = await get_sub_on_file_channels(user_id=call["from"].id, file_id=file.id, bot=call.bot)
    if is_member:
        await send_file(message=call.message, file_id=file.id, state=state, deleted_mes=True)
        await add_channels_click(admin_channel_id=file.user_id, file_id=file.id, with_new_subs=True)
    else:
        await call.answer(language["not_subs"])


def register_subs_on_file_channels_handler(dp: Dispatcher):
    dp.register_callback_query_handler(im_subs, for_key_subs_on_channel.filter(im_subs="True"),
                                       state="get_subscription")
