from tgbot.db.db_com_channel import select_channels
from tgbot.db.db_com_channel_files import count_files, select_files_channels
from tgbot.db.models.file import File


async def file_access_settings(user_id: int, file_id: str) -> dict:
    file = await File.get(file_id)
    channels = await select_channels(user_id=user_id)
    me = file.for_me
    access_type: dict = {"me": me}
    subs = False
    for channel in channels:
        count_file = bool(await select_files_channels(file_id=file_id, channel_id=channel.channel_id))
        subs += count_file
    access_type["subs"] = subs
    if (not subs) and (not me):
        access_type["all"] = True
    else:
        access_type["all"] = False
    return access_type
