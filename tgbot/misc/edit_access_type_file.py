from tgbot.db.db_com_channel_files import delete_channels_file
from tgbot.db.db_com_file import update_file_data
from tgbot.db.models.file import File


async def edit_access_type_file(file_id: str, access_type: str):
    if access_type == "me":
        await delete_channels_file(file_id=file_id)
        await update_file_data(id=file_id, for_me=True)
    elif access_type == "all":
        await delete_channels_file(file_id=file_id)
        await update_file_data(id=file_id, for_me=False)
    elif access_type == "subs":
        await update_file_data(id=file_id, for_me=False)