from random import choice


async def gen_file_id():
    return ''.join(choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-") for i in range(5))
