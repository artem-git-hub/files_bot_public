from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_back, for_key_get_channel


async def return_list_buttons(channels: list):
    inline_keyboard = []

    for channel in channels:
        button = [
            InlineKeyboardButton(
                text=f'✅ {channel["name"]}' if channel["connect"] else f'{channel["name"]}',
                callback_data=for_key_get_channel.new(code="channel_id", id=channel["id"])
            )
        ]
        inline_keyboard.append(button)
    return inline_keyboard


async def def_key_connect_channel_to_file(language: dict, channels: list):
    key_connect_channel_to_file = InlineKeyboardMarkup(
        inline_keyboard=await return_list_buttons(channels=channels) + [
            [
                InlineKeyboardButton(
                    text=f"<<< {language['back']}",
                    callback_data=for_key_back.new(command="back")
                )
            ]
        ]
    )
    return key_connect_channel_to_file
