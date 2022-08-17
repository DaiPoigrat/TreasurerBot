# здесь находятся все хендлеры по обработке действий с админом
from aiogram.types import Message, ContentType, CallbackQuery, InputFile
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin_keyboards import cancelKeyboard, dataBaseKeyboard, chatting_end
from keyboards.inline.init_keyboard import link
from loader import dp, bot
from data.config import ADMINS
from states.states import AdminStates, Chatting
from utils.db_api.create_registry import create_book, get_date
from aiogram.utils.markdown import text


# работа со скачанными файлами
@dp.message_handler(user_id=ADMINS, commands=['dbmanage'], state=None)
async def dataBaseManage(message: Message):
    await message.answer(text="Выберите действие", reply_markup=dataBaseKeyboard)


# обратная связь
@dp.callback_query_handler(user_id=ADMINS, text_contains='chatting_start', state=None)
async def startChatting(call: CallbackQuery, state: FSMContext):
    await state.set_state(Chatting.ToPI)

    data = call.data.split('_')
    user_id = int(data[2])
    user_state = dp.current_state(chat=user_id, user=user_id)
    await user_state.set_state(state=Chatting.ToAdmin)

    username = data[3]
    await state.update_data(
        {"user_id": user_id}
    )
    await call.message.answer(text=f'Начало диалога с {username}')
    await bot.send_message(chat_id=user_id,
                           text='Скоро с вами свяжется Администратор\n'
                                'Диалог будет проходить непосредственно через бота')
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


@dp.message_handler(user_id=ADMINS, state=Chatting.ToPI, content_types=['photo', 'document', 'text'])
async def chatting(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    msg = text(f'<b>Администратор</b>\n{message.text}')

    flag_doc = False
    flag_photo = False

    try:
        # получаем id файла на сервере telegram
        file_id = message.document.file_id
        # задаем описание
        caption = text(f'<b>Администратор</b>\n{message.caption}')
        # отпарвляем документ
        await bot.send_document(chat_id=user_id, document=file_id, caption=caption)

    except:
        flag_doc = True

    try:
        # задаем уникальное имя фотографии
        photo_name = message.photo[-1]["file_unique_id"]
        # получаем id фото
        photo_id = message.photo[-1].file_id
        # задаем описание
        caption = text(f'<b>Администратор</b>\n{message.caption}')
        # отпарвояем фото
        await bot.send_photo(chat_id=user_id, photo=photo_id, caption=caption)
    except:
        flag_photo = True

    # если не фото и не документ
    if flag_doc and flag_photo:
        await bot.send_message(chat_id=user_id, text=msg)


@dp.callback_query_handler(user_id=ADMINS, text_contains='chatting_end', state=Chatting.ToPI)
async def chattingEnd(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    await state.reset_state(with_data=True)
    user_state = dp.current_state(chat=user_id, user=user_id)
    await user_state.reset_state(with_data=True)
    await call.message.answer(text='Система:\nДиалог завершен')
    await bot.send_message(chat_id=user_id, text='Система:\nДиалог завершен', reply_markup=link)
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)
