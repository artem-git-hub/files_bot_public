from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.callback_data import for_key_language, for_key_back


async def def_key_language(language: dict, lang_code: str):
    key_language = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'{language["ru"]} - 🇷🇺' if lang_code != "ru" else f'➡ {language["ru"]} - 🇷🇺 ⬅',
                    callback_data=for_key_language.new("ru")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'{language["en"]} - 🇺🇸 [🇬🇧]' if lang_code != "en" else f'➡ {language["en"]} - 🇺🇸 [🇬🇧] ⬅',
                    callback_data=for_key_language.new("en")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'{language["uk"]} - 🇺🇦' if lang_code != "uk" else f'➡ {language["uk"]} - 🇺🇦 ⬅',
                    callback_data=for_key_language.new("uk")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'{language["be"]} - 🇧🇾' if lang_code != "be" else f'➡ {language["be"]} - 🇧🇾 ⬅',
                    callback_data=for_key_language.new("be")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'<<< {language["back"]}',
                    callback_data=for_key_back.new(command="back")
                )
            ]
        ]
    )
    return key_language
