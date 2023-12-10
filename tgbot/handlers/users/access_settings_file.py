from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.db.db_com_channel import select_channels
from tgbot.db.db_com_channel_files import count_files, select_files_channels, add_file_to_channel, delete_files_channel, \
    delete_files_channels
from tgbot.db.models.file import File
from tgbot.handlers.users.file_keyboard_handler import show_file
from tgbot.keyboards.callback_data import for_key_back, for_key_access_settings, for_key_confirm_cancel, \
    for_key_get_channel
from tgbot.keyboards.inline.key_access_settings import def_key_access_settings
from tgbot.keyboards.inline.key_confirm_cancel import def_key_confirm_cancel
from tgbot.keyboards.inline.key_connect_channel_to_file import def_key_connect_channel_to_file
from tgbot.misc.edit_access_type_file import edit_access_type_file
from tgbot.misc.return_file_access_settings import file_access_settings


async def back_to_file(call: types.CallbackQuery, state: FSMContext):
    await show_file(call=call, state=state)


async def me_file_access(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    file: File = (await state.get_data()).get("file")
    access_type = await file_access_settings(user_id=call.from_user.id, file_id=file.id)
    if access_type["me"]:
        await call.answer(language["access_type_me_good"].format(type_access=language["only_for_me"]))
    elif access_type["subs"]:
        text = language["access_type_me_subs"].format(filename=file.filename)
        await state.set_state("confirm_access_type_me")
        await call.message.edit_text(text=text)
        await call.message.edit_reply_markup(reply_markup=await def_key_confirm_cancel(language=language))
    elif access_type["all"]:
        text = language["access_type_me_all"].format(filename=file.filename)
        await state.set_state("confirm_access_type_me")
        await call.message.edit_text(text=text)
        await call.message.edit_reply_markup(reply_markup=await def_key_confirm_cancel(language=language))


async def confirm_me_file_access(call: types.CallbackQuery, state: FSMContext):
    file: File = (await state.get_data()).get("file")
    await edit_access_type_file(file_id=file.id, access_type="me")
    await cancel_access(call=call, state=state)


async def cancel_access(call: types.CallbackQuery, state: FSMContext):
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


async def subs_file_access(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    file: File = (await state.get_data()).get("file")
    access_type = await file_access_settings(user_id=call.from_user.id, file_id=file.id)
    await state.set_state("confirm_access_type_subs")
    if access_type["all"] or access_type["me"] or access_type["subs"]:
        text = language["access_type_subs_all_me"].format(filename=file.filename)
        user_channels = await select_channels(user_id=call.from_user.id)
        channels = []
        for channel in user_channels:
            channel_info = await call.bot.get_chat(chat_id=channel.channel_id)
            channel_name = channel_info.full_name
            channel_id = channel_info.id
            channel_file = await select_files_channels(file_id=file.id, channel_id=channel_id)
            print(channel_info.full_name, channel_file, "-----------------------------------------------")
            channels.append({"name": channel_name, "id": channel_id, "connect": bool(channel_file)})

        if file.type in ["sticker", "video_note"]:
            await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
            await call.message.edit_text(text=text)
        else:
            await call.message.edit_caption(caption=text)
        await call.message.edit_reply_markup(reply_markup=await def_key_connect_channel_to_file(language=language, channels=channels))




async def get_channel_for_connect(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    file: File = (await state.get_data()).get("file")
    channel_id = callback_data["id"]
    await edit_access_type_file(file_id=file.id, access_type="subs")
    channel_file = await select_files_channels(file_id=file.id, channel_id=channel_id)
    if channel_file:
        await delete_files_channels(channel_id=channel_id, file_id=file.id)
    else:
        await add_file_to_channel(channel_id=channel_id, file_id=file.id)
    await subs_file_access(call=call, state=state)


async def all_file_access(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    file: File = (await state.get_data()).get("file")
    access_type = await file_access_settings(user_id=call.from_user.id, file_id=file.id)
    if access_type["all"]:
        await call.answer(language["access_type_me_good"].format(type_access=language["for_all"]))
    else:
        await call.answer(language["access_type"].format(type_access=language["for_all"]), show_alert=True)
        await edit_access_type_file(file_id=file.id, access_type="all")
        await cancel_access(call=call, state=state)


def register_access_settings_file_handler(dp: Dispatcher):
    dp.register_callback_query_handler(me_file_access, for_key_access_settings.filter(access="me"),
                                       state="access_settings_file")
    dp.register_callback_query_handler(subs_file_access, for_key_access_settings.filter(access="subs"),
                                       state="access_settings_file")
    dp.register_callback_query_handler(all_file_access, for_key_access_settings.filter(access="all"),
                                       state="access_settings_file")

    dp.register_callback_query_handler(confirm_me_file_access, for_key_confirm_cancel.filter(command="confirm"),
                                       state="confirm_access_type_me")
    dp.register_callback_query_handler(cancel_access, for_key_confirm_cancel.filter(command="cancel"),
                                       state="confirm_access_type_me")

    dp.register_callback_query_handler(get_channel_for_connect, for_key_get_channel.filter(code="channel_id"),
                                       state="confirm_access_type_subs")
    dp.register_callback_query_handler(cancel_access, for_key_back.filter(command="back"),
                                       state="confirm_access_type_subs")

    dp.register_callback_query_handler(back_to_file, for_key_back.filter(command="back"), state="access_settings_file")
