from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.db.db_com_channel import select_channel_count_download
from tgbot.db.db_com_file import count_files
from tgbot.db.db_com_files_click import count_files_clicks
from tgbot.db.db_com_user import count_users
from tgbot.keyboards.inline.key_back import def_key_back
from tgbot.states.state_make_newsletter import MakeNewsletter


async def admin_start(message: Message):
    await message.reply("Hello, admin!")


async def get_count_users(message: Message):
    count = await count_users()
    await message.answer(f"Всего юзеров: <code>{count}</code>")


async def get_count_files_clicks(message: Message):
    count = await count_files_clicks()
    await message.answer(f"Всего уникальных кликов: <code>{count}</code>")


async def get_count_files(message: Message):
    count = await count_files()
    await message.answer(f"Всего файлов: <code>{count}</code>")


async def admin_newsletter(message: Message, state: FSMContext):
    language = (await state.get_data()).get("language")
    await message.answer(text="Отправь мне текст рассылки\nЖду >>>", reply_markup=await def_key_back(language=language))
    await MakeNewsletter.get_text.set()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)

    dp.register_message_handler(admin_newsletter, commands=["newsletter"], state="*", is_admin=True)

    dp.register_message_handler(get_count_users, commands=["count_u"], state="*", is_admin=True)
    dp.register_message_handler(get_count_files, commands=["count_f"], state="*", is_admin=True)
    dp.register_message_handler(get_count_files_clicks, commands=["count_fc"], state="*", is_admin=True)
