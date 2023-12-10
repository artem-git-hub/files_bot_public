import asyncio
import random
import re

import aiogram
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentTypes

from tgbot.db.db_com_user import count_users, select_all_users
from tgbot.db.models.user import User
from tgbot.handlers.admin.make_mewsletter import send_admin_newsletter
from tgbot.keyboards.callback_data import for_key_edit_newsletter, for_key_back
from tgbot.keyboards.inline.gen_key_buttons import key_buttons
from tgbot.keyboards.inline.key_back import def_key_back
from tgbot.keyboards.inline.key_reset_all import def_key_reset_all
from tgbot.misc.get_data_file import get_data_file
from tgbot.misc.send_user_file import send_user_file
from tgbot.states.state_make_newsletter import MakeNewsletter


async def show_newsletter(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await send_admin_newsletter(message=call.message, state=state)


async def send_out(call: CallbackQuery, state: FSMContext):
    admin_ids = call.bot.get('config').tg_bot.admin_ids
    language = (await state.get_data()).get("language")
    users = await select_all_users()
    data = await state.get_data()
    newsletter = data["newsletter"]
    count = newsletter["count"]
    channels_list = newsletter["channels_list"]
    block_users = send_users = delete_chat_users = all_user_send = sub_users = deleted_users = 0
    admin_ids = call.bot.get('config').tg_bot.admin_ids
    keyboard = await key_buttons(buttons=newsletter["buttons"], language=language)
    count_all_users = await count_users()

    start_from = random.randint(0, len(users) - count)
    end_to = start_from + count
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 3)
    m = await call.message.answer(f"Рассылка\n\n{all_user_send} / {count}\n\n\n<u>Блокнули: </u>{block_users}\n\n"
                                  f"<u>Удалили чат (или его и не было): </u>{delete_chat_users}\n\n", parse_mode="html")
    for user in users[start_from: end_to]:
        user: User
        try:
            if user.id not in admin_ids:
                if channels_list:
                    no_send = False
                    for channel_id in channels_list:
                        stat = (await call.bot.get_chat_member(chat_id=channel_id, user_id=user.id)).status
                        if stat != "left":
                            no_send = True
                    if not no_send:
                        await send_user_file(message=call.message, file_type=newsletter["f_type"],
                                             tg_id=newsletter["file_id"],
                                             text=newsletter["text"], reply_markup=keyboard,
                                             entities=newsletter["entities"],
                                             custom_user_id=user.id)
                        send_users += 1
                        all_user_send += 1
                    else:
                        sub_users += 1
                        all_user_send += 1
                else:
                    await send_user_file(message=call.message, file_type=newsletter["f_type"],
                                         tg_id=newsletter["file_id"],
                                         text=newsletter["text"], reply_markup=keyboard,
                                         entities=newsletter["entities"],
                                         custom_user_id=user.id)
                    send_users += 1
                    all_user_send += 1
        except aiogram.utils.exceptions.BotBlocked:
            block_users += 1
            all_user_send += 1
        except aiogram.utils.exceptions.UserDeactivated:
            deleted_users += 1
            all_user_send += 1
        except aiogram.utils.exceptions.ChatNotFound:
            delete_chat_users += 1
            all_user_send += 1
        await asyncio.sleep(random.randint(1, 3))
        await m.edit_text(f"Рассылка\n\n{all_user_send} / {count}\n\n\n<u>Блокнули: </u>{block_users}\n\n"
                          f"<u>Удалили чат (или его и не было): </u>{delete_chat_users}\n\n"
                          f"<u>Блокнули + удалили: </u> {block_users + delete_chat_users}\n\n"
                          f"<u>Подписчиков которым не отправилось:</u> {sub_users}\n\n"
                          f"<u>Всего не отправилось: \n(Админы ({len(admin_ids)}) + Блокнули ({block_users}) + Удалили ({delete_chat_users}) + Подписчики ({sub_users}) + Удалённые аккаунты ({deleted_users}): </u> {len(admin_ids) + block_users + delete_chat_users + sub_users + deleted_users}\n\n"
                          f"ИТОГ: \n"
                          f"(отправилось) == {send_users}\n"
                          f"(не отправилось) == {len(admin_ids) + block_users + delete_chat_users + sub_users + deleted_users}\n"
                          f"(хотел отправить) == {all_user_send}\n"
                          f"(всего пользователей в боте) == {count_all_users}", parse_mode="html")
        # await
    await call.message.answer(text=f"Пользователей, которые заблокировали бота: <code>{block_users}</code>\n"
                                   f"Пользователей, которые заблокировали бота и удалили чат: <code>{delete_chat_users}"
                                   f"</code>\n"
                                   f"Пользователей, которым доставлена рассылка: <code>{send_users}</code>\n\n"
                                   f"Удалённые пользователи: <code>{deleted_users}</code>\n\n"
                                   f"Рассылка была на <code>{count}</code> пользователей")


async def edit_text(call: CallbackQuery, state: FSMContext):
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 2)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 3)
    language = (await state.get_data()).get("language")
    await call.message.answer(
        text="Отправь новый текст, или нажми на кнопку чтобы вернуться назад.",
        reply_markup=await def_key_back(language=language))
    await MakeNewsletter.edit_text.set()


async def edit_attached(call: CallbackQuery, state: FSMContext):
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 2)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 3)
    language = (await state.get_data()).get("language")
    await call.message.answer(
        text="Отправь новое вложение или <code>null</code>, или нажми на кнопку чтобы вернуться назад.",
        reply_markup=await def_key_back(language=language))
    await MakeNewsletter.edit_attached.set()


async def edit_button(call: CallbackQuery, state: FSMContext):
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 2)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 3)
    language = (await state.get_data()).get("language")
    await call.message.answer(
        text="Отправь новые кнопки или <code>null</code>\n\nПример:\n"
             "[<b>Кнопка 1 (t.me) - https://t.me/tg_channel </b>\n"
             "<b>Кнопка 2 (ya.ru) - ya.ru </b>]\n\n"
             "или нажми на кнопку чтобы вернуться назад.",
        reply_markup=await def_key_back(language=language))
    await MakeNewsletter.edit_button.set()


async def edit_count(call: CallbackQuery, state: FSMContext):
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 2)
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 3)
    language = (await state.get_data()).get("language")
    c_users = await count_users()
    await call.message.answer(
        text=f"Отправь мне новое кол-во пользователей [ Их всего: <code>{c_users}</code> ]\n\n"
             "или нажми на кнопку чтобы вернуться назад.",
        reply_markup=await def_key_back(language=language))
    await MakeNewsletter.edit_count.set()


async def change_text(message: Message, state: FSMContext):
    data = await state.get_data()
    newsletter = data["newsletter"]
    newsletter["text"] = message.text
    newsletter["entities"] = message.entities
    await state.update_data(newsletter=newsletter)
    await send_admin_newsletter(message=message, state=state)


async def change_attached(message: Message, state: FSMContext):
    tg_id, f_type = await get_data_file(message=message)
    data = await state.get_data()
    newsletter = data["newsletter"]
    newsletter["file_id"] = tg_id
    newsletter["f_type"] = f_type
    await state.update_data(newsletter=newsletter)
    await send_admin_newsletter(message=message, state=state)


async def change_button(message: Message, state: FSMContext):
    text = message.text
    buttons = []
    if text == "null":
        pass
    elif " - " in text and re.search("(http://|ftp://|https://)*[a-z0-9_-]+\.[a-z]{2,10}(/[0-9a-zA-Z-_]*)*", text):
        lines = text.split("\n")
        buttons: list = []
        for line in lines:
            dates = line.split(" - ")
            name_button = dates[0]
            url_button = re.match("(http://|ftp://|https://)*[a-z0-9_-]+\.[a-z]{2,10}(/[0-9a-zA-Z-_]*)*",
                                  dates[1]).group()
            buttons.append({"name": name_button, "url": url_button})
    else:
        await send_admin_newsletter(message=message, state=state)
        return
    data = await state.get_data()
    newsletter = data["newsletter"]
    newsletter["buttons"] = buttons
    await state.update_data(newsletter=newsletter)
    await send_admin_newsletter(message=message, state=state)


async def change_count(message: Message, state: FSMContext):
    print("============================================")
    c_users = await count_users()
    if message.text == "all":
        count = c_users
    else:
        try:
            count = int(message.text)
            c_users = await count_users()
            if count > c_users:
                mes_text = f"Введённое число больше общего кол-ва пользователей\n\n" \
                           f"Все пользователи: {c_users} < Введенное ч-ло: {count}\n\n" \
                           "Попробуй повторно >"

                await message.answer(text=mes_text, reply_markup=await def_key_reset_all())
                await MakeNewsletter.get_count.set()
                return
        except ValueError:
            mes_text = "Не число. \n\nПопробуй повторно >"
            await message.answer(text=mes_text, reply_markup=await def_key_reset_all())
            await MakeNewsletter.get_count.set()
            return
    data = await state.get_data()
    newsletter = data["newsletter"]
    newsletter["count"] = count
    await state.update_data(newsletter=newsletter)
    await send_admin_newsletter(message=message, state=state)


def register_edit_newsletter_handler(dp: Dispatcher):
    dp.register_callback_query_handler(edit_text,
                                       for_key_edit_newsletter.filter(command="edit_text"),
                                       state=MakeNewsletter.changes, is_admin=True)
    dp.register_callback_query_handler(edit_attached,
                                       for_key_edit_newsletter.filter(command="edit_attached"),
                                       state=MakeNewsletter.changes, is_admin=True)
    dp.register_callback_query_handler(edit_button,
                                       for_key_edit_newsletter.filter(command="edit_button"),
                                       state=MakeNewsletter.changes, is_admin=True)
    dp.register_callback_query_handler(edit_count,
                                       for_key_edit_newsletter.filter(command="edit_count"),
                                       state=MakeNewsletter.changes, is_admin=True)

    dp.register_callback_query_handler(show_newsletter,
                                       for_key_back.filter(command="back"),
                                       state=MakeNewsletter.edit_text, is_admin=True)
    dp.register_callback_query_handler(show_newsletter,
                                       for_key_back.filter(command="back"),
                                       state=MakeNewsletter.edit_attached, is_admin=True)
    dp.register_callback_query_handler(show_newsletter,
                                       for_key_back.filter(command="back"),
                                       state=MakeNewsletter.edit_button, is_admin=True)
    dp.register_callback_query_handler(show_newsletter,
                                       for_key_back.filter(command="back"),
                                       state=MakeNewsletter.edit_count, is_admin=True)

    dp.register_message_handler(change_text, state=MakeNewsletter.edit_text, is_admin=True)
    dp.register_message_handler(change_attached,
                                content_types=ContentTypes.AUDIO | ContentTypes.ANIMATION | ContentTypes.DOCUMENT |
                                              ContentTypes.PHOTO | ContentTypes.STICKER | ContentTypes.VIDEO |
                                              ContentTypes.VIDEO_NOTE | ContentTypes.VOICE | ContentTypes.TEXT
                                , state=MakeNewsletter.edit_attached, is_admin=True)
    dp.register_message_handler(change_button, state=MakeNewsletter.edit_button, is_admin=True)
    dp.register_message_handler(change_count, state=MakeNewsletter.edit_count, is_admin=True)

    dp.register_callback_query_handler(send_out,
                                       for_key_edit_newsletter.filter(command="confirm"),
                                       state=MakeNewsletter.changes, is_admin=True)
