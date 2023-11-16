from typing import Union

from sqlalchemy import and_

from tgbot.db.models.channel_files import ChannelFile


async def add_file_to_channel(channel_id: Union[str, int], file_id: str):
    if type(channel_id) == int:
        channel_id = str(channel_id)
    channel = ChannelFile(channel_id=channel_id, file_id=file_id)
    await channel.create()


async def select_file_channels(file_id: str):
    channels = await ChannelFile.query.where(ChannelFile.file_id == file_id).gino.all()
    return channels


async def select_files_channels(file_id: str, channel_id: str):
    if type(channel_id) == int:
        channel_id = str(channel_id)
    files_channels = await ChannelFile.query.where(
        and_(ChannelFile.file_id == file_id, ChannelFile.channel_id == channel_id)).gino.all()
    return files_channels


async def count_files(channel_id: str):
    if type(channel_id) == int:
        channel_id = str(channel_id)
    files = await ChannelFile.query.where(ChannelFile.channel_id == channel_id).gino.all()
    return len(files)


async def delete_files_channel(channel_id: str):
    if type(channel_id) == int:
        channel_id = str(channel_id)
    file_click_stat = await ChannelFile.delete.where(ChannelFile.channel_id == channel_id).gino.status()
    return file_click_stat[0][-1]


async def delete_files_channels(channel_id: str, file_id: str):
    if type(channel_id) == int:
        channel_id = str(channel_id)
    file_click_stat = await ChannelFile.delete.where(
        and_(ChannelFile.channel_id == channel_id, ChannelFile.file_id == file_id)).gino.status()
    return file_click_stat[0][-1]


async def delete_channels_file(file_id: str):
    file_click_stat = await ChannelFile.delete.where(ChannelFile.file_id == file_id).gino.status()
    return file_click_stat[0][-1]
