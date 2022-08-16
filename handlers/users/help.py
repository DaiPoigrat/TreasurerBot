from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS, CFO, TUTOR, ACCOUNTANT
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) in ADMINS:
        text = ("Список команд: ",
                "/dbmanage - управление базой данных")
    elif user_id in CFO:
        text = ("Список команд: ",
                "/toexcel - выгрузить реестр в excel",
                "/agree - согласовать плтежи",
                "/question - связаться с инициатором платежа",
                "/block - заблокировать платеж",
                "/final - выгрузить итоговыый реестр")
    elif user_id in TUTOR:
        text = ("Список команд: ",
                "/agree - согласовать плтежи",
                "/question - связаться с инициатором платежа",
                "/block - заблокировать платеж")
    elif user_id in ACCOUNTANT:
        text = ("Список команд: ",
                "/agree - согласовать плтежи",
                "/question - связаться с инициатором платежа",
                "/block - заблокировать платеж")
    else:
        text = ("Список команд: ",
                "/start - Начать диалог",
                "/help - Получить справку",
                "/payment - заполнить заявку")

    await message.answer("\n".join(text))
