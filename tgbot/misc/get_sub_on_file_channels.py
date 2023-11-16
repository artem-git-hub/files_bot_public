from aiogram import Bot

from tgbot.db.db_com_channel_files import select_file_channels
from tgbot.db.models.channel_files import ChannelFile
from tgbot.db.models.user import User


async def get_sub_on_file_channels(user_id: int, file_id: str, bot: Bot) -> bool:
    file_channels = await select_file_channels(file_id=file_id)
    is_member = True
    for channel in file_channels:
        channel: ChannelFile
        stat = (await bot.get_chat_member(chat_id=channel.channel_id, user_id=user_id)).status
        if stat != "left":
            bool_stat = True
        else:
            bool_stat = False
        is_member *= bool_stat
    return bool(is_member)
