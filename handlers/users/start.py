from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, Message
from states.states import IniciatorStates

from data.config import ADMINS
from keyboards.inline import keys
from loader import dp
from utils.db_api.create_registry import get_date, create_data_record

from aiogram.utils.markdown import text


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.reset_state(with_data=True)
    if str(user_id) in ADMINS:
        await message.answer(text(
            "Это панель администратора.\nПо команде /dbmanage можно увидеть весь функционал."
        ))
    else:
        await message.answer(f"Введите платеж", reply_markup=keys)


@dp.callback_query_handler(text_contains='plan', state='*')
async def getBasisOfPaymentPlan(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {
            "type": 'План',
            "user_id": call.from_user.id
        }
    )
    await call.message.answer(
        "Прикрепите основание оплаты:\n- счет на оплату;\n- акт сверки;\n- чек;\n- скрин транзакции.")
    await IniciatorStates.State1.set()


@dp.callback_query_handler(text_contains='fact', state='*')
async def getBasisOfPaymentFact(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {
            "type": 'Факт',
            "user_id": call.from_user.id
        }
    )
    await call.message.answer(
        "Прикрепите основание оплаты:\n- счет на оплату;\n- акт сверки;\n- чек;\n- скрин транзакции.")
    await IniciatorStates.State1.set()
