from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_confirm_cancel


async def def_key_confirm_cancel(language: dict):
    key_confirm_cancel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"<< {language['back']}",
                    callback_data=for_key_confirm_cancel.new(command="cancel")
                ),

                InlineKeyboardButton(
                    text=language["confirm"],
                    callback_data=for_key_confirm_cancel.new(command="confirm")
                )
            ]
        ]
    )
    return key_confirm_cancel
