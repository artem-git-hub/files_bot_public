from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_channels, for_key_back, for_key_get_channel


async def return_list_buttons(channels: list):
    inline_keyboard = []

    for channel in channels:
        button = [
            InlineKeyboardButton(
                text=channel["name"],
                callback_data=for_key_get_channel.new(code="channel_id", id=channel["id"])
            )
        ]
        inline_keyboard.append(button)
    return inline_keyboard


async def def_key_channels(language: dict, channels: list):
    key_channels = InlineKeyboardMarkup(
        inline_keyboard=await return_list_buttons(channels=channels) + [
            [
                InlineKeyboardButton(
                    text=f"<<< {language['back']}",
                    callback_data=for_key_back.new(command="back")
                ),
                InlineKeyboardButton(
                    text=f"{language['connect']}",
                    callback_data=for_key_channels.new(command="connect")
                )
            ],
        ]
    )
    return key_channels
