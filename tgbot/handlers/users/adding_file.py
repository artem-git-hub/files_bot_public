from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes, ReplyKeyboardRemove
from tgbot.keyboards.callback_data import for_accept_attention
from tgbot.keyboards.inline.key_accept_attention import def_key_accept_attention
from tgbot.misc.send_file import send_file


async def add_file(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language")
    await message.reply(
        text=language["attention"],
        reply_markup=await def_key_accept_attention(language=language))


async def cancel_save_file(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    commands = await call.message.bot.get_my_commands()
    str_commands = str().join(f"\n\n/{i['command']} - <b>{i['description']}</b>" for i in commands)
    await call.message.answer(language["get_com"] + str_commands, reply_markup=ReplyKeyboardRemove())
    await call.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)


async def accept_save_file(call: types.CallbackQuery, state: FSMContext):
    await send_file(message=call.message, with_save=True, state=state, deleted_mes=True)


def register_adding_file(dp: Dispatcher):
    dp.register_message_handler(add_file,
                                content_types=ContentTypes.AUDIO | ContentTypes.ANIMATION | ContentTypes.DOCUMENT |
                                              ContentTypes.PHOTO | ContentTypes.STICKER | ContentTypes.VIDEO |
                                              ContentTypes.VIDEO_NOTE | ContentTypes.VOICE,
                                state="*")
    dp.register_callback_query_handler(accept_save_file, for_accept_attention.filter(command="accept"),
                                       state="*")
    dp.register_callback_query_handler(cancel_save_file, for_accept_attention.filter(command="cancel"),
                                       state="*")
