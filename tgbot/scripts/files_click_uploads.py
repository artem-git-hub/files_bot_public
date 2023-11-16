from tgbot.db.db_com_file import add_file
from tgbot.db.db_com_files_click import add_files_click
from tgbot.db.db_com_user import add_user


async def files_click_on_startapp():
    file = open("tgbot/scripts/files_click.txt")
    for s in file:
        s = s.replace("INSERT INTO public.files_click (id, user_id, file_url, amount, first_time, last_time) VALUES (", "")
        s = s.replace(");", "")
        l = s.split(', ')
        u_id = int(l[1].replace("'", ""))
        f_id = l[2].replace("'", "")
        count = int(l[3].replace("'", ""))
        try:
            await add_files_click(file_id=f_id, user_id=u_id, count=count)
        except Exception as e:
            print(e)


