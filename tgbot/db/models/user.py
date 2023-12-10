from sqlalchemy import Column, BigInteger, String, sql, Boolean
from sqlalchemy.orm import relationship

from tgbot.db.db import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    username = Column(String(100))
    fullname = Column(String(100))
    language = Column(String(10))
    long_id = Column(Boolean, default=False)

    query: sql.Select
