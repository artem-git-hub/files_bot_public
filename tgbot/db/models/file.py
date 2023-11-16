from sqlalchemy import Column, BigInteger, String, sql, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from tgbot.db.db import TimedBaseModel, db
from tgbot.db.models.user import User


class File(TimedBaseModel):
    __tablename__ = "files"

    id = Column(String(100), default="a1", primary_key=True)
    tg_id = Column(String(200), unique=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    type = Column(String(50))
    filename = Column(String(100))
    description = Column(String(1000))
    for_me = Column(Boolean, default=False)

    @declared_attr
    def user(self):
        return relationship(User,
                            primaryjoin=User.id == self.user_id
                            )

    query: sql.Select
