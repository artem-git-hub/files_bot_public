from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.callback_data import for_key_edit_newsletter

key_edit_newsletter = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Изменить текст 📃",
                callback_data=for_key_edit_newsletter.new(command="edit_text")
            ),
            InlineKeyboardButton(
                text="Изменить вложения 🖼",
                callback_data=for_key_edit_newsletter.new(command="edit_attached")
            )
        ],
        [
            InlineKeyboardButton(
                text="Изменить кнопки 🔨",
                callback_data=for_key_edit_newsletter.new(command="edit_button")
            ),
            InlineKeyboardButton(
                text="Изменить кол-во 🔢",
                callback_data=for_key_edit_newsletter.new(command="edit_count")
            )
        ],
        [
            InlineKeyboardButton(
                text="Разослать ✅",
                callback_data=for_key_edit_newsletter.new(command="confirm")
            )
        ]
    ]
)
