from aiogram.dispatcher import FSMContext

from tgbot.db.db_com_languages import select_lang_c
from tgbot.db.models.languages import Languages


async def update_lang_state(state: FSMContext):
    data = await state.get_data()
    lang_code = data.get("lang_code")

    langs = await select_lang_c(land_code=lang_code)
    language = {}
    for l in langs:
        l: Languages
        value = l.value
        # value = value.replace("/*-+-*", "\n")
        value = value.replace("\\n", "\n")
        language[l.code] = value
    await state.update_data(language=language)
