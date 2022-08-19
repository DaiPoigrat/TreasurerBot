# здесь находятся все хендлеры по обработке действий с инициатором
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.inline import payment, chatting_end
from loader import dp, bot
from states.states import IniciatorStates, Chatting

from aiogram.utils.markdown import text
from utils.db_api.create_registry import get_date, create_data_record


# получаем сумму платежа
# @dp.message_handler(state=StateList.AnyState)
@dp.message_handler(state=IniciatorStates.State1, content_types=['photo', 'document', 'text'])
async def getPaymentSum(message: Message, state: FSMContext):
    # флаги, определяющие входной тип данных
    flag_doc = False
    flag_photo = False
    try:
        # получаем id файла на сервере telegram
        file_id = message.document.file_id
        # прописываем имя файла
        file_name = message.document.file_name
        # обновляем данные
        await state.update_data(
            {
                "file_name": file_name,
                "file_id": file_id
            }
        )
    except:
        # если не удалось загрузить документ
        flag_doc = True

    try:
        # задаем уникальное имя фотографии
        photo_name = message.photo[-1]["file_unique_id"]
        photo_id = message.photo[-1].file_id
        # обновляем данные
        await state.update_data(
            {
                "file_name": photo_name,
                "file_id": photo_id
            }
        )
    except:
        # если не удалось загрузить фото
        flag_photo = True

    # если не документ и не фото, значит текстовое описание
    if flag_doc and flag_photo:
        # обновляем данные
        await state.update_data(
            {
                "file_name": message.text,
                "file_id": 'nothing'
            }
        )
    await message.answer("Укажите сумму оплаты")
    await IniciatorStates.State2.set()


# получаем сумму платежа
@dp.message_handler(state=IniciatorStates.State2)
async def getPaymentAmount(message: Message, state: FSMContext):
    # обновляем данные
    await state.update_data(
        {"payment_sum": message.text}
    )
    await message.answer("Укажите размер оплаты", reply_markup=payment)
    await IniciatorStates.State3.set()


# получаем размер оплаты
@dp.callback_query_handler(text_contains='payment', state=IniciatorStates.State3)
async def payment100(call: CallbackQuery, state: FSMContext):
    # вытягиваем данные из коллбека и сохраняем
    await state.update_data(
        {"payment_amount": call.data.split('_')[1]}
    )
    await call.message.answer("Укажите получателя платежа")
    await IniciatorStates.State4.set()
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


# сохраняем получателя платежа
@dp.message_handler(state=IniciatorStates.State4)
async def getPurposeOfPayment(message: Message, state: FSMContext):
    # обновляем данные
    await state.update_data(
        {"payment_recipient": message.text}
    )
    await message.answer("Назначение платежа")
    await IniciatorStates.State5.set()


# получаем назначение платежа
@dp.message_handler(state=IniciatorStates.State5)
async def paymentDeadline(message: Message, state: FSMContext):
    # обновляем данные
    await state.update_data(
        {"purpose_of_payment": message.text}
    )
    await message.answer("Крайний срок оплаты:\n-дд.мм.гггг")
    await IniciatorStates.State6.set()


# получаем крайний срок оплаты
# выход из сбора данныых и очистка состояний
@dp.message_handler(state=IniciatorStates.State6)
async def clearStates(message: Message, state: FSMContext):
    # обновляем данные
    await state.update_data(
        {"payment_deadline": message.text}
    )
    # получаем данные из машины состояний
    data = await state.get_data()
    # создаем новую запись в реестре
    create_data_record(data=data, name=message.from_user.full_name)
    # сообщение пользователю
    await message.answer(text(
        "Заявка в статусе:\n<b>«Принято в оплату»</b>\n\n" +
        '‼️' + "<i>Мы сообщим вам о сроках оплаты и пришлём Платежку с отметкой банка"
               "(если в этом будет необходимость)</i>\n\nСпасибо!"))
    # параметр with_data = False отключает стирание данный в data
    # стираем состояние
    await state.reset_state(with_data=True)
    # имя пользователя
    name = message.from_user.full_name
    # id пользователя
    user_id = message.from_user.id
    # информация по заявке
    msg_text = text(f'Получена новая заявка\nИнформация:\n- Имя: {name}\n- Тип заявки: {data["type"]}')
    # с этой кнопки идет переход в состояние чата через бота(от админа)
    chatting_start = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Написать', callback_data=f'chatting_start_{user_id}_{name}'),
            ]
        ]
    )
    # оповещение админу о новой заявке
    await bot.send_message(chat_id=ADMINS[0], text=msg_text, reply_markup=chatting_start)


# форма отправки сообщения от инициатора админу
@dp.message_handler(state=Chatting.ToAdmin, content_types=['photo', 'document', 'text'])
async def chatting(message: Message, state: FSMContext):
    username = message.from_user.full_name
    # формат текста
    msg = text(f'<b>{username}</b>\n{message.text}')

    flag_doc = False
    flag_photo = False

    try:
        # получаем id файла на сервере telegram
        file_id = message.document.file_id
        # делаем подпись
        caption = text(f'<b>{username}</b>\n{message.caption}')
        # отправляем админу
        await bot.send_document(chat_id=ADMINS[0], document=file_id, caption=caption, reply_markup=chatting_end)
    except:
        # если не удалось отправить документ
        flag_doc = True

    try:
        # задаем уникальное имя фотографии
        photo_name = message.photo[-1]["file_unique_id"]
        # получаем id
        photo_id = message.photo[-1].file_id
        # делаем подпись
        caption = text(f'<b>{username}</b>\n{message.caption}')
        # отправляем админу
        await bot.send_photo(chat_id=ADMINS[0], photo=photo_id, caption=caption, reply_markup=chatting_end)
    except:
        # если не удалось отправить фото
        flag_photo = True

    if flag_doc and flag_photo:
        await bot.send_message(chat_id=ADMINS[0], text=msg, reply_markup=chatting_end)


# отправка сообщения админу об обратной связи
@dp.callback_query_handler(text_contains='link_to_admin')
async def link(call: CallbackQuery):
    # имя пользователя
    name = call.from_user.full_name
    # id пользователя
    user_id = call.from_user.id

    msg_text = text(f'С вами хочет связаться\n{name}')

    link_answer = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Связатсья', callback_data=f'chatting_start_{user_id}_{name}'),
            ]
        ]
    )
    await bot.send_message(chat_id=ADMINS[0], text=msg_text, reply_markup=link_answer)
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)
