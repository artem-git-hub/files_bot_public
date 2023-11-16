from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_back, for_key_access_settings


async def def_key_access_settings(language: dict, access_type: dict):
    key_access_settings = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'✅ {language["only_for_me"]}' if access_type["me"] else f'❌ {language["only_for_me"]}',
                    callback_data=for_key_access_settings.new(access="me")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'✅ {language["only_for_subs"]}' if access_type["subs"] else f'❌ {language["only_for_subs"]}',
                    callback_data=for_key_access_settings.new(access="subs")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'✅ {language["for_all"]}' if access_type["all"] else f'❌ {language["for_all"]}',
                    callback_data=for_key_access_settings.new(access="all")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'< {language["back"]}',
                    callback_data=for_key_back.new(command="back")
                )
            ]
        ]
    )
    return key_access_settings
