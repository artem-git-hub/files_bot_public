import logging

from tgbot.db.db_com_languages import *


async def lang_on_startup():
    try:
        file = open("tgbot/scripts/languages.txt")
        for s in file:
            if s != "\n":
                s = s.split('"')
                code = s[1]
                value = s[3]
                lang_code = s[5]
                lang = await select_lang_c_and_l(code=code, land_code=lang_code)
                if not lang:
                    # value = value.replace("\\n", "/*-+-*")
                    # print(value)
                    await add_lang(code=code, value=value, lang_code=lang_code)
        logging.info("Verification of the table with languages completed successfully!")
    except Exception as e:
        logging.info(" ----------- Error, in table with languages ----------- ")
        logging.info(e)
