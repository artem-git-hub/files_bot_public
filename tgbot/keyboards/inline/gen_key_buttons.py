from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.callback_data import for_key_channels


async def key_buttons(buttons: list, language: list):
    inline_keyboard = []

    for button in buttons:
        but = [
            InlineKeyboardButton(
                text=button["name"],
                url=button["url"]
            )
        ]
        inline_keyboard.append(but)
    keys_buttons = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    keys_buttons.add(InlineKeyboardButton(text=language["delete"],
                                          callback_data=for_key_channels.new(command="delete_newsletter_post")))
    return keys_buttons
