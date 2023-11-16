from sqlalchemy import func, and_

from tgbot.db.models.files_click import FilesClick


async def add_files_click(file_id: str, user_id: int, count: int):
    file_click = FilesClick(file_id=file_id, user_id=user_id, count=count)
    await file_click.create()


async def select_files_clicks(file_id: str):
    files_click = await FilesClick.query.where(FilesClick.file_id == file_id).gino.all()
    return files_click


async def count_files_clicks():
    total = await func.count(FilesClick.id).gino.scalar()
    return total


async def delete_files_clicks(file_id: str):
    file_click_stat = await FilesClick.delete.where(FilesClick.file_id == file_id).gino.status()
    return file_click_stat[0][-1]


async def update_files_click(file_id: str = "", user_id: int = None, count: int = 1):
    files_click = await FilesClick.query.where(
        and_(FilesClick.user_id == user_id, FilesClick.file_id == file_id)).gino.first()

    await files_click.update(count=count).apply()
