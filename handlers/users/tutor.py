# здесь находятся все хендлеры по обработке действий с юристом/куратором
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from keyboards.inline import cfoKeyboard_to_excel, tutorKeyboard_agree, tutorKeyboard_question, tutorKeyboard_block
from keyboards.inline.admin_keyboards import cancelKeyboard, dataBaseKeyboard
from loader import dp
from data.config import TUTOR


# согласовать
@dp.message_handler(user_id=TUTOR, commands=['agree'])
async def dbToExcel(message: Message):
    await message.answer(text='Согласовать:', reply_markup=tutorKeyboard_agree)


# связь с инициатором
@dp.message_handler(user_id=TUTOR, commands=['question'])
async def dbToExcel(message: Message):
    await message.answer(text='Связвться с ... ?', reply_markup=tutorKeyboard_question)


# блок платежа
@dp.message_handler(user_id=TUTOR, commands=['block'])
async def dbToExcel(message: Message):
    await message.answer(text='Заблокировать платеж ... ?', reply_markup=tutorKeyboard_block)


@dp.callback_query_handler(text_contains='accountant_agree_full')
async def agreeFull(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='accountant_agree_separately')
async def agreeSeparately(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='accountant_agree_organisation')
async def agreeOrg(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='accountant_question')
async def question(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='accountant_block')
async def block(call: CallbackQuery):
    pass

