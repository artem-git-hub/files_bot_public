from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link

from tgbot.db.db_com_file import select_file
from tgbot.db.models.file import File
from tgbot.keyboards.inline.key_file import def_key_file
from tgbot.misc.get_clicks import get_clicks


async def edit_count_clicks(call: types.CallbackQuery, state: FSMContext):
    language = (await state.get_data()).get("language")
    data = await state.get_data()
    file: File = data.get("file")
    file_id = file.id
    uniq_clicks, all_clicks = await get_clicks(file_id=file_id)
    file = await select_file(id=file_id)

    id = file.id
    file_type = file.type
    filename = file.filename
    description = f"\n<b>{language['description']}:</b> {file.description}" if file.description != "" else ""

    link = await get_start_link(payload=id)
    text = language['about_file'].format(filename=filename, description=description, file_type=file_type,
                                         link=link, all_clicks=all_clicks, uniq_clicks=uniq_clicks)
    reply_markup = await def_key_file(language=language)

    await state.update_data(file=file, files_click={"uniq_clicks": uniq_clicks, "all_clicks": all_clicks})

    if file.type in ["sticker", "video_note"]:
        await call.message.edit_text(text=text, reply_markup=reply_markup)
    else:
        await call.message.edit_caption(caption=text, reply_markup=reply_markup)
