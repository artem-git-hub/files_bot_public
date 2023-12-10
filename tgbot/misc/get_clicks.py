from tgbot.db.models.files_click import FilesClick


async def get_clicks(file_id: str):
    files_clicks = await FilesClick.query.where(FilesClick.file_id == file_id).gino.all()
    uniq_clicks = len(files_clicks)
    all_clicks = 0
    for click in files_clicks:
        all_clicks += click.count

    return uniq_clicks, all_clicks
