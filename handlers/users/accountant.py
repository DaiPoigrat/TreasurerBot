# здесь находятся все хендлеры по обработке действий с бухгалтером
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from keyboards.inline import cfoKeyboard_to_excel
from keyboards.inline.accountant_keyboard import accountantKeyboard_agree, accountantKeyboard_question, \
    accountantKeyboard_block
from keyboards.inline.admin_keyboards import cancelKeyboard, dataBaseKeyboard
from loader import dp
from data.config import ACCOUNTANT


# согласовать
@dp.message_handler(user_id=ACCOUNTANT, commands=['agree'])
async def dbToExcel(message: Message):
    await message.answer(text='Согласовать:', reply_markup=accountantKeyboard_agree)


# связь с инициатором
@dp.message_handler(user_id=ACCOUNTANT, commands=['question'])
async def dbToExcel(message: Message):
    await message.answer(text='Связвться с ... ?', reply_markup=accountantKeyboard_question)


# блок платежа
@dp.message_handler(user_id=ACCOUNTANT, commands=['block'])
async def dbToExcel(message: Message):
    await message.answer(text='Заблокировать платеж ... ?', reply_markup=accountantKeyboard_block)


@dp.callback_query_handler(text_contains='tutor_agree_full')
async def agreeFull(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='tutor_agree_separately')
async def agreeSeparately(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='tutor_agree_organisation')
async def agreeOrg(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='tutor_question')
async def question(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='tutor_block')
async def block(call: CallbackQuery):
    pass
