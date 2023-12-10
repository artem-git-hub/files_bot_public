from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link

from tgbot.db import db_com_file
from tgbot.db.db_com_file import select_file
from tgbot.keyboards.inline.key_file import def_key_file
from tgbot.keyboards.inline.key_subs_on_channel import def_key_subs_on_channel
from tgbot.misc.add_channel_click import add_channels_click
from tgbot.misc.add_click import add_click
from tgbot.misc.add_to_db_file import add_to_db_file
from tgbot.misc.get_access_types_file import get_access_types_file
from tgbot.misc.get_clicks import get_clicks
from tgbot.misc.get_file_channels import get_file_channels
from tgbot.misc.get_sub_on_file_channels import get_sub_on_file_channels
from tgbot.misc.return_check_access_file import check_access_file
from tgbot.misc.send_user_file import send_user_file


async def send_file(message: types.Message, with_save: bool = False, file_id: str = "", state: FSMContext = None,
                    deleted_mes: bool = False):
    language = (await state.get_data()).get("language")
    if deleted_mes:
        await message.delete()
    if with_save:
        file_dict = await add_to_db_file(message=message.reply_to_message)
        file = await select_file(id=file_dict["id"])
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
    else:
        file = await db_com_file.select_file(id=file_id)
    if file is not None:
        tg_id = file.tg_id
        user_id = file.user_id
        description = f'\n<b>{language["description"]}</b>: {file.description}' if file.description != "" \
            else f'\n<b>{language["description"]}</b>: <code> --- </code>'
        date_add = file.created_at.strftime("%d.%m.%Y | %H:%M:%S")
        date_update = file.updated_at.strftime("%d.%m.%Y | %H:%M:%S")
        uniq_clicks, all_clicks = await get_clicks(file_id=file.id)

        await check_access_file(file_id=file.id)
        await state.update_data(file=file, files_click={"uniq_clicks": uniq_clicks, "all_clicks": all_clicks})

        if (not with_save) and user_id != message.chat.id:
            access_types = await get_access_types_file(file_id=file.id)
            if access_types["me"]:
                text = language["private_file"]
                reply_markup = None
                await message.answer(text=text)
            elif access_types["subs"]:
                is_member = await get_sub_on_file_channels(user_id=message.from_user.id, file_id=file.id,
                                                           bot=message.bot)
                if is_member:
                    await add_channels_click(admin_channel_id=file.user_id, file_id=file.id, with_new_subs=False)
                    await add_click(user_id=message.chat.id, file_id=file.id)
                    text = f"<u>{language['name']}</u>: {file.filename}\n{description}"
                    reply_markup = None
                    await send_user_file(message=message, file_type=file.type, tg_id=tg_id, text=text,
                                         reply_markup=reply_markup)
                else:
                    await state.set_state("get_subscription")
                    text = language["subscription_please"]
                    channels = await get_file_channels(file_id=file.id, bot=message.bot)
                    reply_markup = await def_key_subs_on_channel(language=language, channels=channels)
                    await message.answer(text=text, reply_markup=reply_markup)

            else:
                await add_click(user_id=message.chat.id, file_id=file.id)
                text = f"<u>{language['name']}</u>: {file.filename}\n{description}"
                reply_markup = None
                await send_user_file(message=message, file_type=file.type, tg_id=tg_id, text=text,
                                     reply_markup=reply_markup)
        else:
            link = await get_start_link(payload=file.id)
            text = language['about_file'].format(filename=file.filename, description=description, file_type=file.type,
                                                 link=link, all_clicks=all_clicks, uniq_clicks=uniq_clicks,
                                                 date_add=date_add, date_update=date_update)
            reply_markup = await def_key_file(language=language)
            await send_user_file(message=message, file_type=file.type, tg_id=tg_id, text=text,
                                 reply_markup=reply_markup)


    else:
        await message.answer(text=language["invalid_link"])
