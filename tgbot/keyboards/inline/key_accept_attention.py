from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_accept_attention

async def def_key_accept_attention(language: dict):
    key_accept_attention = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=language["accept"],
                    callback_data=for_accept_attention.new(command="accept")
                )
            ],
            [
                InlineKeyboardButton(
                    text=language["cancel"],
                    callback_data=for_accept_attention.new(command="cancel")
                )
            ]
        ]
    )
    return key_accept_attention
