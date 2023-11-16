from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.db.db_com_user import select_user
from tgbot.db.models.user import User
from tgbot.misc.update_lang_state import update_lang_state


class LoadLanguages(BaseMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    async def on_process_message(self, obj: types.Message, data: dict):
        tg_user = obj.from_user
        state: FSMContext = data.get("state")
        sdata = await state.get_data()
        try:
            lang_code = sdata["lang_code"]
            language = sdata["language"]
        except KeyError:
            user: User = await select_user(id=tg_user.id)
            if user.language == "":
                lang_code = tg_user.language_code if tg_user.language_code in ["ru", "be", "uk", "en"] else "ru"
            else:
                lang_code = user.language
            await state.update_data(lang_code=lang_code)
            await update_lang_state(state=state)

    async def on_process_callback_query(self, obj: types.CallbackQuery, data: dict):
        tg_user = obj["from"]
        state: FSMContext = data.get("state")
        sdata = await state.get_data()
        try:
            lang_code = sdata["lang_code"]
            language = sdata["language"]


            # print("+++++++++++++++++++++++++++++++++++++++++++++++")
            # print(language)
            # print("+++++++++++++++++++++++++++++++++++++++++++++++")


        except KeyError:
            user: User = await select_user(id=tg_user.id)
            if user.language == "":
                lang_code = tg_user.language_code if tg_user.language_code in ["ru", "be", "uk", "en"] else "ru"
            else:
                lang_code = user.language
            await state.update_data(lang_code=lang_code)
            await update_lang_state(state=state)