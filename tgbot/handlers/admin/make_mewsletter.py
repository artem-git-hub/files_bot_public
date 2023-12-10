import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentTypes

from tgbot.db.db_com_channel import select_channels
from tgbot.db.db_com_user import count_users
from tgbot.keyboards.callback_data import for_reset_all, for_key_get_channel, for_key_channels
from tgbot.keyboards.inline.gen_key_buttons import key_buttons
from tgbot.keyboards.inline.key_channels_for_newsletter import def_key_channels_for_newsletter
from tgbot.keyboards.inline.key_edit_newsletter import key_edit_newsletter
from tgbot.keyboards.inline.key_reset_all import def_key_reset_all
from tgbot.misc.get_data_file import get_data_file
from tgbot.misc.send_user_file import send_user_file
from tgbot.states.state_make_newsletter import MakeNewsletter


async def get_text(message: Message, state: FSMContext):
    await state.update_data(newsletter={"text": message.text, "entities": message.entities})
    await message.answer(
        "Текст и его форматирование добавлены\n\nОтправь вложения, без вложений отправь <code>null</code> >>>\n\n"
        "p.s.: отредактировать можно будет всё в конце",
        reply_markup=await def_key_reset_all())
    await MakeNewsletter.get_attached.set()


async def get_attached(message: Message, state: FSMContext):
    tg_id, f_type = await get_data_file(message=message)

    data = await state.get_data()
    newsletter = data["newsletter"]
    newsletter["file_id"] = tg_id
    newsletter["f_type"] = f_type
    await state.update_data(newsletter=newsletter)
    await MakeNewsletter.get_button.set()
    if tg_id is not None:
        await message.answer(
            "Вложения добавлены добавлены\n\nОтправь кнопки, пример: \n\n"
            "[ <b>название кнопки - https://google.com</b> ]\n\n"
            "без кнопок <code>null</code>\n\n"
            "отправь мне количество пользователей на которых делать рассылку\n\n"
            ">>>\n\np.s.: отредактировать можно будет всё в конце",
            reply_markup=await def_key_reset_all())
    else:
        await message.answer(
            "Без вложений\n\nОтправь кнопки, пример: \n"
            "<b>название кнопки - https://google.com</b>\n\n"
            "без кнопок <code>null</code>\n\n"
            "отправь мне количество пользователей на которых делать рассылку\n\n"
            ">>>\n\np.s.: отредактировать можно будет всё в конце",
            reply_markup=await def_key_reset_all())


async def get_button(message: Message, state: FSMContext):
    text = message.text
    mes_text = ""
    c_users = await count_users()

    admin_ids = message.bot.get('config').tg_bot.admin_ids
    if text == "null":
        buttons = []
        mes_text = "<b>Без кнопок</b>\n\nОтправь мне количество пользователей (число, без плавающей точки) на которых " \
                   "будет делаться рассылка, <code>all</code> - для того чтобы разослать по всем пользователям\n\n" \
                   f"Всего пользователей: <code>{c_users}</code>\n" \
                   f"Из них админов (которым не придет сообщение): <code>{len(admin_ids)}</code>"
        data = await state.get_data()
        newsletter = data["newsletter"]
        newsletter["buttons"] = buttons
        await state.update_data(newsletter=newsletter)
    elif " - " in text and re.search("(http://|ftp://|https://)*[a-z0-9_-]+\.[a-z]{2,10}([/]+[0-9a-zA-Z-_]*)*", text):
        lines = text.split("\n")
        buttons: list = []
        for line in lines:
            dates = line.split(" - ")
            name_button = dates[0]
            url_button = re.match("(http://|ftp://|https://)*[a-z0-9_-]+\.[a-z]{2,10}(/[0-9a-zA-Z-_]*)*",
                                  dates[1]).group()
            buttons.append({"name": name_button, "url": url_button})
        data = await state.get_data()
        newsletter = data["newsletter"]
        newsletter["buttons"] = buttons
        await state.update_data(newsletter=newsletter)
        text_button = ""
        for button in buttons:
            text_button += f"<b>{button['name']}</b> --- {button['url']}\n\n"
        mes_text = f"<b>----Кнопки----</b>\n\n{text_button}<b>---------------------</b>\n\nОтправь мне количество" \
                   f" пользователей (<b>число, без плавающей точки</b>) на которых будет делаться рассылка," \
                   f" <code>all</code> - для того чтобы разослать по всем пользователям\n\n" \
                   f"Всего пользователей: <code>{c_users}</code>\n" \
                   f"Из них админов (которым не придет сообщение): <code>{len(admin_ids)}</code>"
    else:
        mes_text = "Походу ты еблан!"
    await message.answer(text=mes_text, reply_markup=await def_key_reset_all())
    await MakeNewsletter.get_count.set()


async def get_count(message: Message, state: FSMContext):
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
    mes_text = f"<b>Кол-во пользователей: <code>{count}</code></b>\n\n" \
               f"Нажми на каналы и выбери по каким не будет идти рассылка" \
               "<code>NULL</code> - для того чтобы не придавать ограничения по каналам нажми на эту кнопку\n\n"
    data = await state.get_data()
    newsletter = data["newsletter"]
    newsletter["count"] = count
    user_channels = await select_channels(user_id=message.from_user.id)
    channels = {}
    channels_list = []
    for channel in user_channels:
        channel_info = await message.bot.get_chat(chat_id=channel.channel_id)
        channel_name = channel_info.full_name
        channel_id = channel_info.id
        channels[channel_id] = {"name": channel_name}
    newsletter["channels"] = channels
    newsletter["channels_list"] = channels_list
    await state.update_data(newsletter=newsletter)
    await message.answer(text=mes_text, reply_markup=await def_key_channels_for_newsletter(channels=channels,
                                                                                           channels_list=channels_list))
    await MakeNewsletter.get_channels.set()


async def get_channel_from_keyboard(call: CallbackQuery, state: FSMContext, callback_data: dict):
    channel_id = callback_data["id"]
    data = await state.get_data()
    newsletter = data["newsletter"]
    channels_list = newsletter["channels_list"]
    channels_list: list
    if channel_id not in channels_list:
        channels_list.append(channel_id)
    else:
        channels_list.remove(channel_id)
    newsletter["channels_list"] = channels_list
    await state.update_data(newsletter=newsletter)
    mes_text = f"<b>Кол-во пользователей: <code>{newsletter['count']}</code></b>\n\n" \
               f"Нажми на каналы и выбери по каким не будет идти рассылка" \
               "<code>NULL</code> - для того чтобы не придавать ограничения по каналам нажми на эту кнопку\n\n"
    await call.message.edit_text(text=mes_text)
    await call.message.edit_reply_markup(
        reply_markup=await def_key_channels_for_newsletter(channels=newsletter["channels"],
                                                           channels_list=newsletter[
                                                               "channels_list"]))


async def send_admin_newsletter(message: Message, state: FSMContext):
    data = await state.get_data()
    newsletter = data["newsletter"]
    language = data["language"]
    channels_list = newsletter["channels_list"]
    channels_text_names = ""
    for channel_id in channels_list:
        channel_info = await message.bot.get_chat(chat_id=channel_id)
        channel_name = channel_info.full_name
        channels_text_names += f"\n<b>{channel_name}</b>"
    keyboard = await key_buttons(buttons=newsletter["buttons"], language=language)
    await message.answer(
        f"_________________НА : <code>{newsletter['count']}</code> : пользователей_____________________")
    await send_user_file(message=message, file_type=newsletter["f_type"], tg_id=newsletter["file_id"],
                         text=newsletter["text"], reply_markup=keyboard, entities=newsletter["entities"])
    await message.answer("______________________________________________________"
                         "\nПо этим каналам:\n"
                         "------------------------------------------------------\n"
                         f"{channels_text_names}\n\n"
                         f"______________________________________________________")
    await message.answer("Изменить рассылку? Или разослать по пользователям?", reply_markup=key_edit_newsletter)
    await MakeNewsletter.changes.set()


async def continue_channels_nlr(call: CallbackQuery, state: FSMContext):
    await send_admin_newsletter(message=call.message, state=state)


async def null_channels_nlr(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    newsletter = data["newsletter"]
    newsletter["channels_list"] = []
    await state.update_data(newsletter=newsletter)
    await MakeNewsletter.get_channels.set()
    await send_admin_newsletter(message=call.message, state=state)


async def cancel_all(call: CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    await state.reset_state(with_data=True)
    await call.message.delete()
    await call.message.answer(text=language["start_mes"])


def register_make_newsletter_handler(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_all, state=MakeNewsletter.get_text, is_admin=True)
    dp.register_callback_query_handler(cancel_all, for_reset_all.filter(command="reset"),
                                       state=MakeNewsletter.get_attached, is_admin=True)
    dp.register_callback_query_handler(cancel_all, for_reset_all.filter(command="reset"),
                                       state=MakeNewsletter.get_button, is_admin=True)
    dp.register_callback_query_handler(cancel_all, for_reset_all.filter(command="reset"),
                                       state=MakeNewsletter.get_count, is_admin=True)

    dp.register_callback_query_handler(get_channel_from_keyboard, for_key_get_channel.filter(code="channel_id"),
                                       state=MakeNewsletter.get_channels, is_admin=True)

    dp.register_callback_query_handler(null_channels_nlr, for_key_channels.filter(command="null"),
                                       state=MakeNewsletter.get_channels, is_admin=True)
    dp.register_callback_query_handler(continue_channels_nlr, for_key_channels.filter(command="continue"),
                                       state=MakeNewsletter.get_channels, is_admin=True)

    dp.register_message_handler(get_text, state=MakeNewsletter.get_text, is_admin=True)
    dp.register_message_handler(get_attached,
                                content_types=ContentTypes.AUDIO | ContentTypes.ANIMATION | ContentTypes.DOCUMENT |
                                              ContentTypes.PHOTO | ContentTypes.STICKER | ContentTypes.VIDEO |
                                              ContentTypes.VIDEO_NOTE | ContentTypes.VOICE | ContentTypes.TEXT
                                , state=MakeNewsletter.get_attached, is_admin=True)
    dp.register_message_handler(get_button, state=MakeNewsletter.get_button, is_admin=True)
    dp.register_message_handler(get_count, state=MakeNewsletter.get_count, is_admin=True)
