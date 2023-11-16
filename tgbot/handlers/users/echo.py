from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode


async def bot_echo(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language")
    text = language["oy_shit"]
    await state.reset_state()
    await message.answer(text=text)


async def bot_echo_all(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language")
    state_name = await state.get_state()
    text = language["oy_shit"]
    await state.reset_state()
    await message.answer(text=text)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
