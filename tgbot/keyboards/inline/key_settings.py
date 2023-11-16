from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_settings


async def def_key_settings(language: dict, long_id: bool = False):
    key_settings = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=language["lang"],
                    callback_data=for_key_settings.new("edit_language")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{language['conn_channel']}",
                    callback_data=for_key_settings.new("plug_channel")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{language['long_id']} ❌" if not long_id else f"{language['long_id']} ✅",
                    callback_data=for_key_settings.new("edit_long_id")
                )
            ],
        ]
    )
    return key_settings