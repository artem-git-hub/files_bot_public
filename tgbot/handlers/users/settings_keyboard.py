from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.db.db_com_channel import select_channels
from tgbot.db.db_com_user import update_user_data, select_user
from tgbot.db.models.user import User
from tgbot.keyboards.callback_data import for_key_settings, for_key_language, for_key_back
from tgbot.keyboards.inline.key_channels import def_key_channels
from tgbot.keyboards.inline.key_language import def_key_language
from tgbot.keyboards.inline.key_settings import def_key_settings
from tgbot.misc.update_lang_state import update_lang_state


async def edit_long_id(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    user = await select_user(id=call["from"].id)
    long_id = user.long_id
    if long_id:
        long_id = False
    else:
        long_id = True
    await update_user_data(id=call["from"].id, long_id=long_id)
    await call.message.edit_reply_markup(reply_markup=await def_key_settings(language=language, long_id=long_id))


async def edit_language(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    lang_code = (await state.get_data()).get("lang_code")
    await state.set_state("get_lang")
    await call.message.delete()
    await call.message.answer(text=language["lang_text"],
                              reply_markup=await def_key_language(language=language, lang_code=lang_code))


async def plug_channel(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    user_channels = await select_channels(user_id=call["from"].id)
    channels = []
    for channel in user_channels:
        channel_info = await call.bot.get_chat(chat_id=channel.channel_id)
        channel_name = channel_info.full_name
        channel_id = channel_info.id
        channels.append({"name": channel_name, "id": channel_id})
    text = language["plug_channel"]
    await state.set_state("get_channel")
    await call.message.edit_text(text=text)
    await call.message.edit_reply_markup(reply_markup=await def_key_channels(language=language, channels=channels))


async def get_language(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await state.reset_state(with_data=False)
    lang = callback_data["lang"]
    await update_user_data(id=call["from"].id, language=lang)
    await state.update_data(lang_code=lang)
    await update_lang_state(state=state)
    await edit_language(call=call, state=state)


async def back_to_settings(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    user = await User.get(call["from"].id)
    long_id = user.long_id
    await state.reset_state(with_data=False)
    await call.message.delete()
    await call.message.answer(text=language["set_mes"],
                              reply_markup=await def_key_settings(language=language, long_id=long_id))


def register_settings_keyboard_handler(dp: Dispatcher):
    dp.register_callback_query_handler(edit_language, for_key_settings.filter(command="edit_language"), state="*")
    dp.register_callback_query_handler(edit_long_id, for_key_settings.filter(command="edit_long_id"), state="*")
    dp.register_callback_query_handler(plug_channel, for_key_settings.filter(command="plug_channel"), state="*")

    dp.register_callback_query_handler(get_language, for_key_language.filter(lang="ru"), state="get_lang")
    dp.register_callback_query_handler(get_language, for_key_language.filter(lang="en"), state="get_lang")
    dp.register_callback_query_handler(get_language, for_key_language.filter(lang="uk"), state="get_lang")
    dp.register_callback_query_handler(get_language, for_key_language.filter(lang="be"), state="get_lang")

    dp.register_callback_query_handler(back_to_settings, for_key_back.filter(command="back"), state="get_lang")
