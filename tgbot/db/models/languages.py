from sqlalchemy import Column, String, Integer

from tgbot.db.db import TimedBaseModel


class Languages(TimedBaseModel):
    __tablename__ = "languages"

    id = Column(Integer, autoincrement=True, primary_key=True)
    code = Column(String(50))
    value = Column(String)
    lang_code = Column(String(2))
