from aiogram import types
from aiogram.types import ReplyKeyboardMarkup


async def send_user_file(message: types.Message, file_type: str, tg_id: str, text: str,
                         reply_markup: ReplyKeyboardMarkup, entities=None, custom_user_id: int = None):
    if custom_user_id:
        user_id = custom_user_id
    else:
        user_id = message.chat.id
    if file_type == "audio":
        await message.bot.send_audio(chat_id=user_id, audio=tg_id, caption=text, caption_entities=entities,
                                     reply_markup=reply_markup)
    elif file_type == "animation":
        await message.bot.send_animation(chat_id=user_id, animation=tg_id, caption=text, caption_entities=entities,
                                         reply_markup=reply_markup)
    elif file_type == "document":
        await message.bot.send_document(chat_id=user_id, document=tg_id, caption=text, caption_entities=entities,
                                        reply_markup=reply_markup)
    elif file_type == "photo":
        await message.bot.send_photo(chat_id=user_id, photo=tg_id, caption=text, caption_entities=entities,
                                     reply_markup=reply_markup)
    elif file_type == "sticker":
        await message.bot.send_sticker(chat_id=user_id, sticker=tg_id)
        await message.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup, entities=entities,
                                       disable_web_page_preview=True)
    elif file_type == "video":
        await message.bot.send_video(chat_id=user_id, video=tg_id, caption=text, caption_entities=entities,
                                     reply_markup=reply_markup)
    elif file_type == "video_note":
        await message.bot.send_video_note(chat_id=user_id, video_note=tg_id)
        await message.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup, entities=entities,
                                       disable_web_page_preview=True)
    elif file_type == "voice":
        await message.bot.send_voice(chat_id=user_id, voice=tg_id, caption=text, caption_entities=entities,
                                     reply_markup=reply_markup)
    elif file_type == "null":
        await message.bot.send_message(chat_id=user_id, text=text, entities=entities, reply_markup=reply_markup)
