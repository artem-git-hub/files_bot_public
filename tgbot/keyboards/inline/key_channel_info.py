from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_channel_info, for_key_back


async def def_key_channel_info(language: dict):
    key_channel_info = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{language['delete']}",
                    callback_data=for_key_channel_info.new(command="delete")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"< {language['back']}",
                    callback_data=for_key_back.new(command="back")
                )
            ],
        ]
    )
    return key_channel_info
