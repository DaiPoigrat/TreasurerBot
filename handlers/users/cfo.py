# здесь находятся все хендлеры по обработке действий с cfo
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from keyboards.inline import cfoKeyboard_to_excel, cfoKeyboard_agree, cfoKeyboard_question, cfoKeyboard_block
from keyboards.inline.admin_keyboards import cancelKeyboard, dataBaseKeyboard
from loader import dp
from data.config import CFO


# выгрузить реестр в excel
@dp.message_handler(user_id=CFO, commands=['toexcel'])
async def dbToExcel(message: Message):
    await message.answer(text='Выгрузить базу данных?', reply_markup=cfoKeyboard_to_excel)


# согласовать
@dp.message_handler(user_id=CFO, commands=['agree'])
async def paymentAgree(message: Message):
    await message.answer(text='Согласовать:', reply_markup=cfoKeyboard_agree)


# связь с инициатором
@dp.message_handler(user_id=CFO, commands=['question'])
async def linkToIniciator(message: Message):
    await message.answer(text='Связвться с ... ?', reply_markup=cfoKeyboard_question)


# блок платежа
@dp.message_handler(user_id=CFO, commands=['block'])
async def paymentBlock(message: Message):
    await message.answer(text='Заблокировать платеж ... ?', reply_markup=cfoKeyboard_block)


# выгрузить итоговый реестр в excel
@dp.message_handler(user_id=CFO, commands=['final'])
async def dbToExcel(message: Message):
    await message.answer(text='Выгрузить итоговый реестр?', reply_markup=cfoKeyboard_to_excel)


@dp.callback_query_handler(text_contains='cfo_agree_full')
async def agreeFull(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='cfo_agree_separately')
async def agreeSeparately(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='cfo_agree_organisation')
async def agreeOrg(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='cfo_question')
async def question(call: CallbackQuery):
    pass


@dp.callback_query_handler(text_contains='cfo_block')
async def block(call: CallbackQuery):
    pass
