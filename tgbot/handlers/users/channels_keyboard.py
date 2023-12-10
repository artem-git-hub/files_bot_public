import logging
import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from sqlalchemy import and_

from tgbot.db.db_com_channel import add_channel, select_channel_count_download, delete_channel
from tgbot.db.db_com_channel_files import count_files, delete_files_channel
from tgbot.db.models.channel import Channel
from tgbot.db.models.user import User
from tgbot.handlers.users.settings_keyboard import plug_channel
from tgbot.keyboards.callback_data import for_key_back, for_key_channels, for_key_get_channel, for_key_channel_info, \
    for_key_confirm_cancel
from tgbot.keyboards.inline.key_back import def_key_back
from tgbot.keyboards.inline.key_channel_info import def_key_channel_info
from tgbot.keyboards.inline.key_confirm_cancel import def_key_confirm_cancel
from tgbot.keyboards.inline.key_settings import def_key_settings


async def connect_channel(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    await state.set_state("get_message_from_channel")
    bot_username = call.message["from"].username
    text = language["connect_channel_mes"].format(bot_username=bot_username)
    await call.message.edit_text(text=text)
    await call.message.edit_reply_markup(reply_markup=await def_key_back(language=language))


async def channel_info(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    language = (await state.get_data()).get("language")
    count_channel_download = await select_channel_count_download(channel_id=callback_data["id"],
                                                                 user_id=call.from_user.id)
    chat = await call.bot.get_chat(chat_id=callback_data["id"])
    await state.update_data(chat_id=chat.id)
    channel_name = chat.full_name
    chat_type = chat.type.upper()
    chat_id = chat.id
    all_count_download = count_channel_download["count_download"]
    sub_count_download = count_channel_download["count_sub_download"]
    count_file = await count_files(channel_id=chat_id)
    await call.message.edit_text(
        text=language["channel_info_mes"].format(chat_id=chat_id, channel_name=channel_name, chat_type=chat_type,
                                                 count_file=count_file,
                                                 all_count_download=all_count_download,
                                                 sub_count_download=sub_count_download))
    await call.message.edit_reply_markup(reply_markup=await def_key_channel_info(language=language))
    await state.set_state("channel_info")


async def get_forwarded_message(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language")
    try:
        pattern = "https://t.me/[\w_]*"
        if message.text is None or "https://t.me" not in message.text:
            channel_id = message.forward_from_chat.id
            # print("=====================================================")
        elif re.findall(pattern=pattern, string=message.text):
            username_group = message.text.split("/")[-1]
            group = await message.bot.get_chat(chat_id=f"@{username_group}")
            print(group)
            channel_id = group.id
        user_id = message.from_user.id
        channel = await Channel.query.where(
            and_(Channel.user_id == str(user_id), Channel.channel_id == str(channel_id))).gino.all()
        if channel:
            await message.answer(text=language["channel_is_connect"],
                                 reply_markup=await def_key_back(language=language))
        else:
            await add_channel(user_id=user_id, channel_id=channel_id)
            await message.answer(text=language["good_connect_channel"],
                                 reply_markup=await def_key_back(language=language))
    except Exception as e:
        logging.info(e)
        await message.answer(text=language["ebat_connect_channel"], reply_markup=await def_key_back(language=language))


async def back_channels(call: types.CallbackQuery, state: FSMContext):
    await plug_channel(call=call, state=state)


async def cancel_delete_channel(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    chat_id = (await state.get_data()).get("chat_id")
    callback_data["id"] = chat_id
    await channel_info(call=call, state=state, callback_data=callback_data)


async def confirm_delete_channel(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    chat_id = (await state.get_data()).get("chat_id")
    if any([await delete_files_channel(channel_id=chat_id),
            await delete_channel(channel_id=chat_id, user_id=call.from_user.id)]):
        await call.answer(language["good_delete_channel"])
        await back_channels(call=call, state=state)
    else:
        await call.answer(text=language["no_good_delete_channel"], show_alert=True)
        await back_channels(call=call, state=state)


async def deletes_channel(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    chat_id = (await state.get_data()).get("chat_id")
    chat = await call.bot.get_chat(chat_id=chat_id)
    await state.set_state("delete_channel")
    await call.message.edit_text(text=language["delete_channel"].format(channel_name=chat.full_name))
    await call.message.edit_reply_markup(reply_markup=await def_key_confirm_cancel(language=language))


async def back_settings(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    user = await User.get(call["from"].id)
    long_id = user.long_id
    await state.reset_state(with_data=False)
    await call.message.delete()
    await call.message.answer(text=language["set_mes"],
                              reply_markup=await def_key_settings(language=language, long_id=long_id))


def register_channels_keyboard_handler(dp: Dispatcher):
    dp.register_callback_query_handler(back_settings, for_key_back.filter(command="back"), state="get_channel")
    dp.register_callback_query_handler(back_channels, for_key_back.filter(command="back"),
                                       state="get_message_from_channel")
    dp.register_callback_query_handler(back_channels, for_key_back.filter(command="back"),
                                       state="channel_info")

    dp.register_callback_query_handler(deletes_channel, for_key_channel_info.filter(command="delete"),
                                       state="channel_info")

    dp.register_callback_query_handler(confirm_delete_channel, for_key_confirm_cancel.filter(command="confirm"),
                                       state="delete_channel")
    dp.register_callback_query_handler(cancel_delete_channel, for_key_confirm_cancel.filter(command="cancel"),
                                       state="delete_channel")

    dp.register_message_handler(get_forwarded_message,
                                content_types=ContentTypes.AUDIO | ContentTypes.ANIMATION | ContentTypes.DOCUMENT |
                                              ContentTypes.PHOTO | ContentTypes.STICKER | ContentTypes.VIDEO |
                                              ContentTypes.VIDEO_NOTE | ContentTypes.VOICE | ContentTypes.TEXT,
                                state="get_message_from_channel")

    dp.register_callback_query_handler(connect_channel, for_key_channels.filter(command="connect"), state="get_channel")

    dp.register_callback_query_handler(channel_info, for_key_get_channel.filter(code="channel_id"),
                                       state="get_channel")
