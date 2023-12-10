import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType

from tgbot.db import db_com_files_click, db_com_file
from tgbot.db.db_com_file import count_files
from tgbot.db.models.file import File
from tgbot.keyboards.callback_data import for_key_file, for_key_back, for_key_confirm_cancel
from tgbot.keyboards.inline.key_access_settings import def_key_access_settings
from tgbot.keyboards.inline.key_back import def_key_back
from tgbot.keyboards.inline.key_confirm_cancel import def_key_confirm_cancel
from tgbot.misc.edit_count_clicks import edit_count_clicks
from tgbot.misc.get_clicks import get_clicks
from tgbot.misc.get_user_files import get_user_files
from tgbot.misc.return_file_access_settings import file_access_settings
from tgbot.misc.send_file import send_file


async def edit_name(call: CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    data = await state.get_data()
    file: File = data.get("file")
    filename = file.filename
    if file.type in ["video_note", "sticker"]:
        await call.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
    await call.message.delete()
    await state.set_state("give_name")
    await call.message.answer(
        text=language["get_name"].format(filename=filename),
        reply_markup=await def_key_back(language=language))


async def edit_description(call: CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    data = await state.get_data()
    file: File = data.get("file")
    description = file.description if file.description != "" else f"<code>{language['not_des']}</code>"
    if file.type in ["video_note", "sticker"]:
        await call.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
    await call.message.delete()
    await state.set_state("give_description")
    await call.message.answer(
        text=language["get_des"].format(description=description),
        reply_markup=await def_key_back(language=language))


async def show_file(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    file: File = data.get("file")
    file_id = file.id
    await state.reset_state(with_data=False)
    language = (await state.get_data()).get("language")
    await send_file(message=call.message, file_id=file_id, state=state, deleted_mes=True)


async def get_name(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language")
    if len(message.text) > 100:
        await state.set_state("give_name")
        await message.answer(text=language["invalid_name"], reply_markup=await def_key_back(language=language))
    else:
        data = await state.get_data()
        file: File = data.get("file")
        await db_com_file.update_file_data(id=file.id, filename=message.text)
        await state.set_state("give_name")
        await message.answer(
            text=language["valid_name"],
            reply_markup=await def_key_back(language=language))


async def get_description(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language")
    await state.set_state("give_description")
    if len(message.text) > 1000:
        await message.answer(text=language["invalid_des"], reply_markup=await def_key_back(language=language))
    else:
        data = await state.get_data()
        file: File = data.get("file")
        await db_com_file.update_file_data(id=file.id, description=message.text)
        await message.answer(
            text=language["valid_des"],
            reply_markup=await def_key_back(language=language))


async def show_all_files(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(num_list=0, filetype="")
    data = await state.get_data()
    file: File = data.get("file")
    if file.type in ["sticker", "video_note"]:
        await call.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
    await get_user_files(message=call.message, state=state, from_call=True)


async def delete_file(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    await call.message.delete()
    await state.set_state("delete_file")
    await call.message.answer(text=language["delete_this"],
                              reply_markup=await def_key_confirm_cancel(language=language))


async def confirm_delete_file(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    data = await state.get_data()
    file: File = data.get("file")
    stat_files_click = await db_com_files_click.delete_files_clicks(file_id=file.id)
    stat_file = await db_com_file.delete_file(id=file.id)
    # print(stat_file, stat_files_click)
    if stat_file:
        await call.answer(language["good_del"])
    else:
        logging.info(msg=f"Возникла ошибка при удалении файла: {file.id = }")
        await call.answer(language["error_file"])
    await state.reset_state(with_data=False)
    await state.update_data(num_list=0, filetype="")
    if file.type in ["sticker", "video_note"]:
        await call.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 2)
    await get_user_files(message=call.message, state=state, from_call=True)


async def cancel_delete_file(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    file: File = data.get("file")
    await state.reset_state(with_data=False)
    await send_file(call.message, file_id=file.id, state=state, deleted_mes=True)


async def access_settings_file(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get("language")
    file: File = data.get("file")
    filename = file.filename
    text = language["access_settings_file"].format(filename=filename)
    await state.set_state("access_settings_file")
    reply_markup = await def_key_access_settings(language=language,
                                                 access_type=await file_access_settings(user_id=call.from_user.id,
                                                                                        file_id=file.id))
    if file.type in ["sticker", "video_note"]:
        await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
        await call.message.edit_text(text=text)
    else:
        await call.message.edit_caption(caption=text)
    await call.message.edit_reply_markup(reply_markup=reply_markup)


async def update_file(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    data = await state.get_data()
    file: File = data.get("file")
    if file:
        files_click: dict = data.get("files_click")
        uniq_clicks_old = files_click["uniq_clicks"]
        all_clicks_old = files_click["all_clicks"]
        uniq_clicks_new, all_clicks_new = await get_clicks(file_id=file.id)
        if all_clicks_old == all_clicks_new and uniq_clicks_old == uniq_clicks_new:
            await call.answer(text=language["no_changes"])
        else:
            await edit_count_clicks(call=call, state=state)


def register_file_keyboard_handler(dp: Dispatcher):
    dp.register_callback_query_handler(edit_name, for_key_file.filter(command="edit_name"), state="*")
    dp.register_callback_query_handler(edit_description, for_key_file.filter(command="edit_description"), state="*")
    dp.register_callback_query_handler(show_all_files, for_key_file.filter(command="my_files"), state="*")
    dp.register_callback_query_handler(delete_file, for_key_file.filter(command="delete"), state="*")
    dp.register_callback_query_handler(update_file, for_key_file.filter(command="update"), state="*")
    dp.register_callback_query_handler(access_settings_file, for_key_file.filter(command="access_settings"), state="*")

    dp.register_callback_query_handler(confirm_delete_file, for_key_confirm_cancel.filter(command="confirm"),
                                       state="delete_file")
    dp.register_callback_query_handler(cancel_delete_file, for_key_confirm_cancel.filter(command="cancel"),
                                       state="delete_file")

    dp.register_callback_query_handler(show_file, for_key_back.filter(command="back"), state="give_name")
    dp.register_callback_query_handler(show_file, for_key_back.filter(command="back"), state="give_description")

    dp.register_message_handler(get_name, content_types=ContentType.TEXT, state="give_name")
    dp.register_message_handler(get_description, content_types=ContentType.TEXT, state="give_description")
