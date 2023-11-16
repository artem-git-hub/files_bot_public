from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.callback_data import for_key_get_channel, for_key_channels


async def return_list_buttons(channels: dict, channels_list: list):
    inline_keyboard = []

    for channel in channels:
        button = [
            InlineKeyboardButton(
                text=f"✅ {channels[channel]['name']}" if str(channel) in channels_list else f"❌ {channels[channel]['name']}",
                callback_data=for_key_get_channel.new(code="channel_id", id=channel)
            )
        ]
        inline_keyboard.append(button)
    return inline_keyboard


async def def_key_channels_for_newsletter(channels: dict, channels_list: list):
    key_channels = InlineKeyboardMarkup(
        inline_keyboard=await return_list_buttons(channels=channels, channels_list=channels_list) + [
            [
                InlineKeyboardButton(
                    text=f"NULL",
                    callback_data=for_key_channels.new(command="null")
                ),
                InlineKeyboardButton(
                    text=f"Продолжить",
                    callback_data=for_key_channels.new(command="continue")
                )
            ],
        ]
    )
    return key_channels
