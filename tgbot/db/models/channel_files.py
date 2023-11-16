from sqlalchemy import Column, Integer, String

from tgbot.db.db import TimedBaseModel


class ChannelFile(TimedBaseModel):
    __tablename__ = "channel_files"

    id = Column(Integer, autoincrement=True, primary_key=True)
    channel_id = Column(String(15))
    file_id = Column(String(100))
