from typing import Union

from sqlalchemy import and_

from tgbot.db.models.channel import Channel


async def add_channel(user_id: Union[str, int], channel_id: Union[str, int], count_download: int = 0,
                      count_sub_download: int = 0):
    if type(user_id) == int:
        user_id = str(user_id)
    if type(channel_id) == int:
        channel_id = str(channel_id)
    channel = Channel(user_id=user_id, channel_id=channel_id, count_download=count_download,
                      count_sub_download=count_sub_download)
    await channel.create()


async def select_channels(user_id: Union[str, int]):
    if type(user_id) == int:
        user_id = str(user_id)
    channels = await Channel.query.where(Channel.user_id == user_id).gino.all()
    return channels


async def select_channel(user_id: Union[str, int], channel_id: Union[str, int]):
    if type(user_id) == int:
        user_id = str(user_id)
    if type(channel_id) == int:
        channel_id = str(channel_id)
    channel = await Channel.query.where(and_(Channel.user_id == user_id, Channel.channel_id == channel_id)).gino.first()
    return channel


async def select_channel_count_download(channel_id: Union[str, int], user_id: Union[str, int]):
    if type(channel_id) == int:
        channel_id = str(channel_id)
    if type(user_id) == int:
        user_id = str(user_id)
    channel = await Channel.query.where(and_(Channel.user_id == user_id, Channel.channel_id == channel_id)).gino.first()
    count_download = {"count_download": channel.count_download, "count_sub_download": channel.count_sub_download}
    return count_download


async def delete_channel(user_id: str, channel_id: str):
    if type(channel_id) == int:
        channel_id = str(channel_id)
    if type(user_id) == int:
        user_id = str(user_id)
    channel_stat = await Channel.delete.where(
        and_(Channel.user_id == user_id, Channel.channel_id == channel_id)).gino.status()
    return channel_stat[0][-1]


async def update_channel_data(user_id: Union[str, int], channel_id: str, all_click: int = None, new_subs_click: int = None):
    if type(channel_id) == int:
        channel_id = str(channel_id)
    if type(user_id) == int:
        user_id = str(user_id)
    channel = await Channel.query.where(
        and_(Channel.user_id == user_id, Channel.channel_id == channel_id)).gino.first()
    if all_click:
        await channel.update(count_download=all_click).apply()
    if new_subs_click:
        await channel.update(count_sub_download=new_subs_click).apply()
