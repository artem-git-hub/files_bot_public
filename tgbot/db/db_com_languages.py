from sqlalchemy import and_

from tgbot.db.models.languages import Languages


async def add_lang(code: str, value: str, lang_code: str):
    lang = Languages(code=code, value=value, lang_code=lang_code)
    await lang.create()


async def select_lang_id(id: str):
    lang = await Languages.query.where(Languages.id == id).gino.first()
    return lang


async def select_lang_c_and_l(code: str, land_code: str):
    lang = await Languages.query.where(and_(Languages.code == code, Languages.lang_code == land_code)).gino.first()
    return lang


async def select_lang_c(land_code: str):
    langs = await Languages.query.where(Languages.lang_code == land_code).gino.all()
    return langs


async def delete_lang(id: str):
    file_stat = await Languages.delete.where(Languages.id == id).gino.status()
    return file_stat[0][-1]


async def update_file_data(id: str, code: str = None, value: str = None, lang_code: str = None):
    lang = await Languages.get(id)
    if code:
        await lang.update(code=code).apply()
    if value:
        await lang.update(value=value).apply()
    if lang_code:
        await lang.update(lang_code=lang_code).apply()
