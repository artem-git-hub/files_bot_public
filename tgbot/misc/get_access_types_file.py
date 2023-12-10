from tgbot.db.db_com_channel_files import select_file_channels
from tgbot.db.models.file import File


async def get_access_types_file(file_id: str) -> dict:
    file = await File.get(file_id)
    file_channels = await select_file_channels(file_id=file_id)
    me = file.for_me
    access_types: dict = {"me": me}
    subs = bool(file_channels)
    access_types["subs"] = subs
    if (not subs) and (not me):
        access_types["all"] = True
    else:
        access_types["all"] = False
    return access_types
