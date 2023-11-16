from typing import List

import sqlalchemy as sa
from aiogram import Dispatcher
import logging
from aiogram.utils.executor import Executor
from gino import Gino
from sqlalchemy import Column, DateTime, func

logger = logging.getLogger(__name__)
db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=func.now())
    updated_at = Column(
        DateTime(True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
    )


async def on_startup(dispatcher: Dispatcher):
    logger.info("Setup PostgreSQL Connection")
    config = dispatcher.bot["config"]
    postgres_uri = f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}"
    await db.set_bind(postgres_uri)


async def on_shutdown():
    bind = db.pop_bind()
    if bind:
        logger.info("Close PostgreSQL Connection")
        await bind.close()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
