from sqlalchemy import Column, BigInteger, String, sql, ForeignKey, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from tgbot.db.db import TimedBaseModel
from tgbot.db.models.file import File
from tgbot.db.models.user import User


class FilesClick(TimedBaseModel):
    __tablename__ = "files_clicks"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    file_id = Column(String(100), ForeignKey('files.id'))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    count = Column(Integer)

    @declared_attr
    def user(self):
        return relationship(User,
                            primaryjoin=User.id == self.user_id
                            )

    @declared_attr
    def file(self):
        return relationship(File,
                            primaryjoin=File.id == self.file_id
                            )

    query: sql.Select
