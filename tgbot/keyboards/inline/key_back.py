from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_back


async def def_key_back(language: dict):
    key_back = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'< {language["back"]}',
                    callback_data=for_key_back.new(command="back")
                )
            ]
        ]
    )
    return key_back
