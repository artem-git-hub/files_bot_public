from tgbot.db.db_com_user import add_user


async def users_on_startapp():
    file = open("tgbot/scripts/users.txt")
    for s in file:
        s = s.replace("INSERT INTO public.users (id, user_id, username, time_reg) VALUES (", "")
        s = s.replace(");", "")
        l = s.split(', ')
        username = l[2].replace("'", "")
        u_id = int(l[1])
        # print(l[1], l[2], l[2].replace("'", ""))
        await add_user(id=u_id, username=username if username != "None" else "")
