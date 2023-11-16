from aiogram import Bot

from tgbot.db.db_com_channel_files import select_file_channels
from tgbot.db.models.channel_files import ChannelFile


async def get_file_channels(file_id: str, bot: Bot) -> list:
    file_channels = await select_file_channels(file_id=file_id)
    channels = []
    for channel in file_channels:
        channel: ChannelFile
        chat = await bot.get_chat(chat_id=channel.channel_id)
        if chat.type == "channel":
            channels.append({"name": chat.full_name, "link": chat.invite_link})
        else:
            channels.append({"name": chat.full_name, "link": f"t.me/{chat.username}"})
    return channels
