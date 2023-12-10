from sqlalchemy import and_

from tgbot.db import db_com_files_click as db_click

from tgbot.db.models.files_click import FilesClick


async def add_click(user_id: int, file_id: str):
    click = await FilesClick.query.where(
        and_(FilesClick.user_id == user_id, FilesClick.file_id == file_id)).gino.first()
    if click is None:
        await db_click.add_files_click(file_id=file_id, user_id=user_id, count=1)
    else:
        await db_click.update_files_click(file_id=file_id, user_id=user_id, count=click.count + 1)
