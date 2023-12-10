from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_navigation_files, for_get_type


async def key_navigation_files(user_types: Union[list, set], with_navigation: bool = False):
    file_types = {
        "photo": "photo",
        "video": "video",
        "audio": "audio",
        "sticker": "stick",
        "document": "_doc_",
        "video_note": "krug_",
        "animation": "_gif_",
        "voice": "voice",
        "unsort": "  ✖  "
    }
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=file_types[type],
                    callback_data=for_get_type.new(type=type)
                ) for type in user_types[:4] if len(user_types) > 1
            ],

            [] if user_types[4:8] != [] else [
                InlineKeyboardButton(
                    text=file_types[type],
                    callback_data=for_get_type.new(type=type)
                ) for type in user_types[4:8]
            ],
            [
                InlineKeyboardButton(
                    text="<<<",
                    callback_data=for_key_navigation_files.new(command="previous")
                ),
                InlineKeyboardButton(
                    text=">>>",
                    callback_data=for_key_navigation_files.new(command="next")
                ),
            ] if with_navigation else []
        ]
    )












    # keyboard = InlineKeyboardMarkup(
    #     inline_keyboard=[
    #         [
    #             InlineKeyboardButton(
    #                 text="stick",
    #                 callback_data=for_get_type.new(type="sticker")
    #             ),
    #             InlineKeyboardButton(
    #                 text="krug_",
    #                 callback_data=for_get_type.new(type="video_note")
    #             ),
    #             InlineKeyboardButton(
    #                 text="animation",
    #                 callback_data=for_get_type.new(type="_gif_")
    #             ),
    #             InlineKeyboardButton(
    #                 text="video",
    #                 callback_data=for_get_type.new(type="video")
    #             ),
    #         ],
    #
    #         [
    #             InlineKeyboardButton(
    #                 text="voice",
    #                 callback_data=for_get_type.new(type="voice")
    #             ),
    #             InlineKeyboardButton(
    #                 text="audio",
    #                 callback_data=for_get_type.new(type="audio")
    #             ),
    #             InlineKeyboardButton(
    #                 text="photo",
    #                 callback_data=for_get_type.new(type="photo")
    #             ),
    #             InlineKeyboardButton(
    #                 text="_doc_",
    #                 callback_data=for_get_type.new(type="document")
    #             ),
    #         ],
    #         [
    #             InlineKeyboardButton(
    #                 text="<<<",
    #                 callback_data=for_key_navigation_files.new(command="previous")
    #             ),
    #             InlineKeyboardButton(
    #                 text=">>>",
    #                 callback_data=for_key_navigation_files.new(command="next")
    #             ),
    #         ]
    #     ]
    # )
    #















    # keyboard_line = []
    # for i in list(file_types.keys())[:4]:
    #     keyboard_line.append(InlineKeyboardButton(
    #         text=file_types[i],
    #         callback_data=for_get_type.new(type=i)
    #     ))
    # keyboard.row(keyboard_line)
    # if len(list(file_types.keys())) > 4:
    #     keyboard_line = []
    #     for i in list(file_types.keys())[:4]:
    #         keyboard_line.append(InlineKeyboardButton(
    #             text=file_types[i],
    #             callback_data=for_get_type.new(type=i)
    #         ))
    #     keyboard.row(keyboard_line)
    # keyboard.row(
    #     InlineKeyboardButton(
    #         text="<<<",
    #         callback_data=for_key_navigation_files.new(command="previous")
    #     ),
    #     InlineKeyboardButton(
    #         text=">>>",
    #         callback_data=for_key_navigation_files.new(command="next")
    #     )
    # )
    return keyboard
