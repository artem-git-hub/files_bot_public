from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Перезапуск | Restart"),
            types.BotCommand("mf", "Мои файлы | My files"),
            types.BotCommand("settings", "Настройки | Some settings"),
            types.BotCommand("help", "Спасити памагити | Some help"),
        ]
    )
