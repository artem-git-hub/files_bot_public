from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link
from sqlalchemy import and_
import math
from tgbot.db.models.file import File
from tgbot.keyboards.inline.key_navigation_files import key_navigation_files


async def get_user_files(message: types.Message, state: FSMContext, from_call: bool = False, edit: bool = False):
    language = (await state.get_data()).get("language")
    if from_call:
        await message.delete()
    user_id = message.chat.id
    data = await state.get_data()
    num_list = data.get("num_list")
    filetype = data.get("filetype")
    # print(num_list, filetype)
    files = await File.query.where(File.user_id == user_id).gino.all()
    user_types = set()
    for file in files:
        user_types.add(file.type)
    if filetype:
        user_types.remove(filetype)
        user_types = list(user_types)
        user_types += ["unsort"]
    user_types = list(user_types)
    if filetype != "":
        files = await File.query.where(and_(File.user_id == user_id, File.type == filetype)).gino.all()
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
    text = language["user_files"]
    if (num_list * 8) + 1 > len(files):
        num_list = 0
    elif (((num_list + 1) * 8) + 1) <= 1:
        num_list = ((len(files) - 1) // 8)

    await state.update_data(num_list=num_list, filetype=filetype)

    for i in range((num_list * 8) + 1, ((num_list + 1) * 8) + 1):
        try:
            file = files[i - 1]
            s = ""
            file_type = file_types[file.type]
            date = file.created_at.strftime("%d.%m.%y")
            link = await get_start_link(payload=file.id)
            str_i = f"{i}".ljust(5, " ")
            s += f"\n\n{str_i} - <code>({file_type})</code> - <code>{date}</code> - <b><a href='{link}'>(click ⏩) " \
                 f"{file.filename}</a></b>"
            text += s
        except IndexError:
            break

    number = language["no_page"]
    text += f"\n\n<u><i>{number}</i> {num_list + 1}</u> / <u>{math.ceil(len(files) / 8)}</u>"

    with_navigation = True
    if len(files) <= 8:
        with_navigation = False

    if edit:
        await message.edit_text(text=text, reply_markup=await key_navigation_files(user_types=user_types,
                                                                                   with_navigation=with_navigation),
                                disable_web_page_preview=True)
    else:
        await message.answer(text=text, reply_markup=await key_navigation_files(user_types=user_types,
                                                                                with_navigation=with_navigation),
                             disable_web_page_preview=True)
