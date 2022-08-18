from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) in ADMINS:
        text = ("Список команд: ",
                "/dbmanage - управление базой данных")
    else:
        text = ("Список команд: ",
                "/start - Начать диалог",
                "/help - Получить справку")

    await message.answer("\n".join(text))
