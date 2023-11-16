from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

import tgbot.db.db_com_user as db_user
from tgbot.db.db_com_channel import select_channel_count_download
from tgbot.db.models.user import User
from tgbot.keyboards.inline.key_settings import def_key_settings
from tgbot.misc.get_sub_on_file_channels import get_sub_on_file_channels
from tgbot.misc.get_user_files import get_user_files


async def user_start(message: Message, state: FSMContext):
    language = (await state.get_data()).get("language")
    # await get_sub_on_file_channels(user_id=message.from_user.id, file_id="l3WH4", bot=message.bot)
    # await message.answer(text=f'{language["start_mes"]}', reply_markup=InlineKeyboardMarkup(
    #     inline_keyboard=[[InlineKeyboardButton(text="user ➖", url="tg://chat?id=1684324679")]]))
    await message.answer(text=language["start_mes"])
    await db_user.add_user(id=message.from_user.id,
                           username=message.from_user.username if message.from_user.username is not None else "",
                           fullname=message.from_user.full_name)


async def get_all_files(message: types.Message, state: FSMContext):
    await state.update_data(num_list=1, filetype="")
    await get_user_files(message=message, state=state)


async def user_help(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language")
    await message.answer(text=language["help_mes"])


async def user_settings(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language")
    user = await User.get(message.from_user.id)
    long_id = user.long_id
    await message.answer(text=language["set_mes"],
                         reply_markup=await def_key_settings(language=language, long_id=long_id))


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_all_files, commands=["mf"], state="*")
    dp.register_message_handler(user_help, commands=["help"], state="*")
    dp.register_message_handler(user_settings, commands=["settings"], state="*")
