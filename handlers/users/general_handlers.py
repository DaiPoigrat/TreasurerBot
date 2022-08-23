# здесь прописываются хендлеры, общие для всех управляющих ролей
import logging

from aiogram.types import Message, ContentType, File, CallbackQuery, InputFile, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import text

from data.config import ADMINS
from keyboards.inline import registries, cancelKeyboard, iniciators, files
from loader import dp, bot
from utils.db_api.db_manage import write_to_excel, drop_excel
from states.states import AdminStates
from utils.db_api.create_registry import get_date, create_book
import os
import psycopg2
from data.config import DB_URI


# отправить реестр
@dp.callback_query_handler(user_id=ADMINS, text_contains='download_register')
async def downloadRegistry(call: CallbackQuery):
    doc = InputFile(path_or_bytesio='data/register.xlsx')
    await call.message.answer_document(document=doc)
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(user_id=ADMINS, text_contains='download_db')
async def downloadRegistry(call: CallbackQuery):
    write_to_excel()
    doc = InputFile(path_or_bytesio='data/database.xlsx')
    await call.message.answer_document(document=doc)
    await bot.answer_callback_query(call.id)
    drop_excel()


@dp.callback_query_handler(user_id=ADMINS, text_contains='update_register', state=None)
async def getRegistry(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text('<b>Система</b>\nПришлите excel документ'))
    await AdminStates.UploadFile.set()
    await bot.answer_callback_query(call.id)


@dp.message_handler(user_id=ADMINS, state=AdminStates.UploadFile, content_types=['document'])
async def updateDataBase(message: Message, state: FSMContext):
    try:
        file_id = message.document.file_id
        file = await bot.get_file(file_id=file_id)
        await bot.download_file(file_path=file.file_path, destination='data/register.xlsx')
        await message.answer(text('<b>Система</b>\nДанные успешно обновлены!'))
    except Exception as err:
        await message.answer(text('<b>Система</b>\nПроизошла ошибка, обратитесь к администратору!'))
        logging.exception(err)
    finally:
        await state.reset_state(with_data=True)


# скачивание рееста
@dp.callback_query_handler(user_id=ADMINS, text_contains='get_registry')
async def downloadRegistry(call: CallbackQuery):
    filename = call.data.split('_')[2]
    register = InputFile(path_or_bytesio=f'registries/{filename}')
    await call.message.answer_document(document=register)
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


# выбор инициатора
@dp.callback_query_handler(user_id=ADMINS, text_contains='download_files')
async def chooseIniciator(call: CallbackQuery):
    await call.message.answer(text=text('<b>Система</b>\nВыберите инициатора из списка'), reply_markup=iniciators())
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(user_id=ADMINS, text_contains='iniciator_')
async def chooseFile(call: CallbackQuery):
    iniciator = call.data.split('_')[1]
    await call.message.answer(text=text('<b>Система</b>\nВыберите нужный файл'),
                              reply_markup=files(iniciator=iniciator))
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(user_id=ADMINS, text_contains='download_file_')
async def downloadFile(call: CallbackQuery):
    unic_id = call.data.split('_')[2]
    try:
        db_connection = psycopg2.connect(DB_URI, sslmode="require")
        db_object = db_connection.cursor()

        db_object.execute(
            f"SELECT file_id FROM register WHERE callback_id = {unic_id}"
        )
        # id файла на сервере телеги
        result = db_object.fetchone()[0].rstrip()
        # костыль на отпрвку файлов и фото
        try:
            await call.message.answer_document(document=result)
        except:
            await call.message.answer_photo(photo=result)

    except Exception as err:
        logging.exception(err)

    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


# обработка команды отмена со всех клавиатур
@dp.callback_query_handler(text_contains='cancel', state='*')
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    # возврат пустой клавиатуры
    await call.message.edit_reply_markup(reply_markup=None)
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)
