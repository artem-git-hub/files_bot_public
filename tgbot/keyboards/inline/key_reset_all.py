from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_reset_all


async def def_key_reset_all():
    key_reset_all = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Сбросить всё",
                    callback_data=for_reset_all.new(command="reset")
                )
            ],
        ]
    )
    return key_reset_all
