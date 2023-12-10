from sqlalchemy import Column, Integer, String

from tgbot.db.db import TimedBaseModel


class Channel(TimedBaseModel):
    __tablename__ = "channels"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String(11))
    channel_id = Column(String(15))
    count_download = Column(Integer, default=0)
    count_sub_download = Column(Integer, default=0)
