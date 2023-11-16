from dataclasses import dataclass

from environs import Env
from typing import List


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    debug: bool


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    config = Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str("DB_NAME"),
            debug=env.bool("DEBUG")
        ),
        misc=Miscellaneous()
    )
    # config.db[
    #     "postgres_uri"] = f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}"
    return config
