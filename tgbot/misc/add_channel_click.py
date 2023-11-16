from tgbot.db.db_com_channel import select_channel, update_channel_data
from tgbot.db.db_com_channel_files import select_file_channels
from tgbot.db.models.channel import Channel


async def add_channels_click(admin_channel_id: int, file_id: str, with_new_subs: bool = False):
    file_channels = await select_file_channels(file_id=file_id)
    for chat in file_channels:
        channel: Channel = await select_channel(user_id=admin_channel_id, channel_id=chat.channel_id)
        all_click = channel.count_download + 1
        new_subs_click = channel.count_sub_download + 1
        await update_channel_data(user_id=admin_channel_id, channel_id=channel.channel_id, all_click=all_click)
        if with_new_subs:
            await update_channel_data(user_id=admin_channel_id, channel_id=channel.channel_id,
                                      new_subs_click=new_subs_click)