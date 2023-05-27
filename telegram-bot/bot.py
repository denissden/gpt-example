from aiogram import Bot


static: Bot = None


def save_static(bot: Bot):
    global static
    static = bot
