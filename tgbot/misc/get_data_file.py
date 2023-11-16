from aiogram.types import Message

from tgbot.misc.gen_name_file import gen_name_file


async def get_data_file(message: Message, get_filename: bool = False):
    tg_id = filename = file_type = ""
    if message.content_type == "audio":
        tg_id = message.audio.file_id
        filename = message.audio.file_name
        file_type = "audio"

    elif message.content_type == "animation":
        tg_id = message.animation.file_id
        filename = message.animation.file_name
        file_type = "animation"

    elif message.content_type == "document":
        tg_id = message.document.file_id
        filename = message.document.file_name
        file_type = "document"

    elif message.content_type == "photo":
        tg_id = message.photo[-1].file_id
        filename = await gen_name_file(user_id=message.from_user.id, type="photo")
        file_type = "photo"

    elif message.content_type == "sticker":
        tg_id = message.sticker.file_id
        filename = await gen_name_file(user_id=message.from_user.id, type="sticker")
        file_type = "sticker"

    elif message.content_type == "video":
        tg_id = message.video.file_id
        filename = message.video.file_name
        file_type = "video"

    elif message.content_type == "video_note":
        tg_id = message.video_note.file_id
        filename = await gen_name_file(user_id=message.from_user.id, type="video_note")
        file_type = "video_note"

    elif message.content_type == "voice":
        tg_id = message.voice.file_id
        filename = await gen_name_file(user_id=message.from_user.id, type="voice")
        file_type = "voice"

    elif message.text is not None:
        if message.text == "null":
            tg_id = None
            file_type = "null"
        else:
            await message.answer("Не обрабатываемый тип")
            return

    if get_filename:
        return tg_id, filename, file_type
    else:
        return tg_id, file_type
