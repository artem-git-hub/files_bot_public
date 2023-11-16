from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.callback_data import for_get_type, for_key_navigation_files
from tgbot.misc.get_user_files import get_user_files


async def sort_by_type(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    language = (await state.get_data()).get("language")
    file_types = {
        "photo": "photo",
        "video": "video",
        "audio": "audio",
        "sticker": "stick",
        "document": "_doc_",
        "video_note": "krug_",
        "animation": "_gif_",
        "voice": "voice"
    }
    if callback_data["type"] != "unsort":
        filetype = callback_data["type"]
        await call.answer(text=f"{language['sort_on']} {file_types[filetype]}")
    else:
        filetype = ""
        await call.answer(text=language['sort_off'])
    await state.update_data(num_list=0, filetype=filetype)
    await get_user_files(message=call.message, state=state, edit=True)


async def navigation(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    command = callback_data["command"]
    data = await state.get_data()
    num_list = data.get("num_list")
    if num_list is not None:
        if command == "previous":
            await state.update_data(num_list=num_list - 1)
        else:
            await state.update_data(num_list=num_list + 1)
        await get_user_files(message=call.message, state=state, edit=True)
    else:
        await state.update_data(num_list=0, filetype="")
        await get_user_files(message=call.message, state=state, edit=True)


def register_navigation_keyboard_handler(dp: Dispatcher):
    dp.register_callback_query_handler(sort_by_type, for_get_type.filter(type="photo"), state="*")
    dp.register_callback_query_handler(sort_by_type, for_get_type.filter(type="video"), state="*")
    dp.register_callback_query_handler(sort_by_type, for_get_type.filter(type="audio"), state="*")
    dp.register_callback_query_handler(sort_by_type, for_get_type.filter(type="sticker"), state="*")
    dp.register_callback_query_handler(sort_by_type, for_get_type.filter(type="document"), state="*")
    dp.register_callback_query_handler(sort_by_type, for_get_type.filter(type="video_note"), state="*")
    dp.register_callback_query_handler(sort_by_type, for_get_type.filter(type="animation"), state="*")
    dp.register_callback_query_handler(sort_by_type, for_get_type.filter(type="voice"), state="*")
    dp.register_callback_query_handler(sort_by_type, for_get_type.filter(type="unsort"), state="*")

    dp.register_callback_query_handler(navigation, for_key_navigation_files.filter(command="previous"), state="*")
    dp.register_callback_query_handler(navigation, for_key_navigation_files.filter(command="next"), state="*")
