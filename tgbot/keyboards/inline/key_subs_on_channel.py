from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.callback_data import for_key_subs_on_channel


async def return_list_buttons(channels: list):
    inline_keyboard = []

    for channel in channels:
        button = [
            InlineKeyboardButton(
                text=channel["name"],
                url=channel["link"]
            )
        ]
        inline_keyboard.append(button)
    return inline_keyboard


async def def_key_subs_on_channel(language: dict, channels: list):
    key_subs_on_channel = InlineKeyboardMarkup(
        inline_keyboard=await return_list_buttons(channels=channels) + [
            [
                InlineKeyboardButton(
                    text=f"{language['im_subs']} ✅",
                    callback_data=for_key_subs_on_channel.new(im_subs="True")
                )
            ],
        ]
    )
    return key_subs_on_channel
