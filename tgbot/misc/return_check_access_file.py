from tgbot.db.db_com_channel_files import select_file_channels, delete_channels_file
from tgbot.db.models.file import File


async def check_access_file(file_id: str):
    file = await File.get(file_id)
    channels_file = await select_file_channels(file_id=file_id)
    if file.for_me and bool(channels_file):
        await delete_channels_file(file_id=file_id)
