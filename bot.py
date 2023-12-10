import asyncio
import logging

import tenacity
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.db.db import db
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin.edit_newsletter import register_edit_newsletter_handler
from tgbot.handlers.admin.make_mewsletter import register_make_newsletter_handler
from tgbot.handlers.users.access_settings_file import register_access_settings_file_handler
from tgbot.handlers.users.adding_file import register_adding_file
from tgbot.handlers.admin.admin import register_admin
from tgbot.handlers.users.channels_keyboard import register_channels_keyboard_handler
from tgbot.handlers.users.delete_newsletter_post import register_del_newsletter_post_handler
from tgbot.handlers.users.echo import register_echo
from tgbot.handlers.users.commands import register_user
from tgbot.handlers.users.file_keyboard_handler import register_file_keyboard_handler
from tgbot.handlers.users.navigation_keyboard_handler import register_navigation_keyboard_handler
from tgbot.handlers.users.settings_keyboard import register_settings_keyboard_handler
from tgbot.handlers.users.subs_on_file_channels import register_subs_on_file_channels_handler
from tgbot.handlers.users.take_link import register_take_link
from tgbot.middlewares.debug_message import DebugMes
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.load_languages import LoadLanguages
from tgbot.middlewares.only_user import OnlyUser
from tgbot.middlewares.update_user_data import UpdateUserData
from tgbot.misc.set_bot_commands import set_default_commands
from tgbot.scripts.file_uploads import files_on_startapp
from tgbot.scripts.files_click_uploads import files_click_on_startapp
from tgbot.scripts.upload_lang import lang_on_startup
from tgbot.scripts.user_uploads import users_on_startapp

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(OnlyUser())
    dp.setup_middleware(UpdateUserData())
    dp.setup_middleware(LoadLanguages())
    dp.setup_middleware(DebugMes())
    # dp.setup_middleware(RemoveWatch())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_del_newsletter_post_handler(dp)
    register_edit_newsletter_handler(dp)
    register_take_link(dp)
    register_subs_on_file_channels_handler(dp)
    register_channels_keyboard_handler(dp)
    register_settings_keyboard_handler(dp)
    register_make_newsletter_handler(dp)
    register_adding_file(dp)
    register_file_keyboard_handler(dp)
    register_navigation_keyboard_handler(dp)
    register_access_settings_file_handler(dp)
    register_admin(dp)
    register_user(dp)
    register_echo(dp)


async def wait_postgres(config):
    postgres_url = f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}"
    await db.set_bind(postgres_url)
    if config.db.debug:
        await db.gino.drop_all()
        await db.gino.create_all()
        # await users_on_startapp()
        # await files_on_startapp()
        # await files_click_on_startapp()
    version = await db.scalar("SELECT version();")
    logger.info("Connected to {postgres}".format(postgres=version))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot.")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    # db

    logger.info("Database connection. Wait for PostgreSQL...")
    try:
        await wait_postgres(config=config)
    except tenacity.RetryError:
        logger.error("Failed to establish connection with PostgreSQL.")
        exit(1)
    logger.info("Ready. Successful database connection.")

    bot['config'] = config
    # bot['state'] = dp.storage

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    await lang_on_startup()

    await set_default_commands(dp)
    # start
    await dp.bot.send_message("1652127583", "Бот запущен!")
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
