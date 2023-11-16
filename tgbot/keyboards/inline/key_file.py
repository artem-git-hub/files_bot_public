from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_file


async def def_key_file(language: dict):
    key_file = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=language["edit_name"],
                    callback_data=for_key_file.new(command="edit_name")
                )
            ],

            [
                InlineKeyboardButton(
                    text=language["edit_des"],
                    callback_data=for_key_file.new(command="edit_description")
                )
            ],

            [
                InlineKeyboardButton(
                    text=language["access_settings"],
                    callback_data=for_key_file.new(command="access_settings")
                )
            ],

            [
                InlineKeyboardButton(
                    text=language["my_files"],
                    callback_data=for_key_file.new(command="my_files")
                )
            ],
            [
                InlineKeyboardButton(
                    text=language["delete"],
                    callback_data=for_key_file.new(command="delete")
                ),
                InlineKeyboardButton(
                    text=language["update"],
                    callback_data=for_key_file.new(command="update")
                )
            ]
        ]
    )
    return key_file
