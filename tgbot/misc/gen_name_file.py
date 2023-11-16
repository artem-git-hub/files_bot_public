from sqlalchemy import and_
import re
from tgbot.db.models.file import File


async def gen_name_file(user_id: int, type: str):
    files = await File.query.where(and_(File.user_id == user_id, File.type == type)).gino.all()
    pattern = "{}\s[(]\d+[)]".format(type)
    max_num = -1
    for i in files:

        if re.findall(pattern=pattern, string=i.filename.split(".")[0]):
            filename = i.filename
            new_filename = filename.replace("{type} (".format(type=type), "")
            pattern = '[)][.0-9a-zA-Z_]*'
            del_element = re.findall(pattern=pattern, string=new_filename)[0]

            str_num = new_filename.replace(del_element, "")
            num = int(str_num)

            max_num = max(max_num, num + 1)
    if max_num == -1:
        max_num += 2
    return str("{type} ({num})".format(type=type, num=max_num))
