from tgbot.db.db_com_file import add_file
from tgbot.db.db_com_user import add_user


async def files_on_startapp():
    file = open("tgbot/scripts/files.txt")
    for s in file:
        s = s.replace("INSERT INTO public.files (id, user_id, type, file_id, file_url, description, time_add, file_name) VALUES (", "")
        s = s.replace(");", "")
        l = s.split(', ')
        # print(l)
        f_type = l[2].replace("'", "")
        f_id = l[3].replace("'", "")
        f_url = l[4].replace("'", "")
        u_id = l[1].replace("'", "")
        f_name = l[7].replace("'", "")
        # print(u_id)
        try:
            await add_file(id=f_url, tg_id=f_id, user_id=int(u_id), type=f_type, filename=f_name)
        except Exception as e:
            print(e)


