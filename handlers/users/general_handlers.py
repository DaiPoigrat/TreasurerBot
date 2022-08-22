# здесь прописываются хендлеры, общие для всех управляющих ролей
import logging

from aiogram.types import Message, ContentType, File, CallbackQuery, InputFile, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.inline import registries, cancelKeyboard, iniciators, files
from loader import dp, bot
from utils.db_api.db_manage import write_to_excel, drop_excel
from states.states import AdminStates
from utils.db_api.create_registry import get_date, create_book, set_active_registry, get_active_registry, readBuffer, \
    writeBuffer
import os
import psycopg2
from data.config import DB_URI


# # считывание названия
# @dp.callback_query_handler(user_id=ADMINS, text_contains='create_book', state=None)
# async def setNewRegistryName(call: CallbackQuery, state: FSMContext):
#     await call.message.answer(text='Введите название рестра без расширения', reply_markup=cancelKeyboard)
#     await AdminStates.EnterName.set()
#     # избавляемся от часиков
#     await bot.answer_callback_query(call.id)
#
#
# # создание рееста
# @dp.message_handler(user_id=ADMINS, state=AdminStates.EnterName)
# async def createNewRegistry(message: Message, state: FSMContext):
#     registry_name = message.text + '.xlsx'
#     try:
#         if registry_name in os.listdir('registries'):
#             await message.answer(text='Реестр с таким названием уже существует.\nПожалуйста, введите другое!')
#     except:
#         pass
#     else:
#         create_book(name=registry_name)
#         await state.reset_state(with_data=True)
#
#         choice = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [
#                     InlineKeyboardButton(text='Да', callback_data=f'set_registry_{registry_name}'),
#                     InlineKeyboardButton(text='Нет', callback_data='cancel'),
#                 ]
#             ]
#         )
#         await message.answer(text='Реестр успешно создан!\nСделать его активным?', reply_markup=choice)


# # делает реестр активным
# @dp.callback_query_handler(user_id=ADMINS, text_contains='set_registry')
# async def setActive(call: CallbackQuery):
#     filename = call.data.split('_')[2]
#     set_active_registry(new_active=filename)
#     await call.message.answer(f'Активный реестр:\n{filename}')
#     # избавляемся от часиков
#     await bot.answer_callback_query(call.id)


#


@dp.callback_query_handler(user_id=ADMINS, text_contains='download_register')
async def downloadRegistry(call: CallbackQuery):
    write_to_excel()
    doc = InputFile(path_or_bytesio='data/register.xlsx')
    await call.message.answer_document(document=doc)
    drop_excel()


# обработка команды отмена со всех клавиатур
@dp.callback_query_handler(text_contains='cancel')
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    # возврат пустой клавиатуры
    await call.message.edit_reply_markup(reply_markup=None)
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(user_id=ADMINS, text_contains='update_register', state=None)
async def getRegistry(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Пришлите excel документ')
    await AdminStates.UploadFile.set()
    await bot.answer_callback_query(call.id)


@dp.message_handler(user_id=ADMINS, state=AdminStates.UploadFile)
async def updateDataBase(message: Message, state: FSMContext):
    file_id = message.document.file_id
    file = bot.get_file(file_id=file_id)
    logging.info(msg=f'file = {file_id}')
    await state.reset_state(with_data=True)


# # выбор нужного реестра
# @dp.callback_query_handler(user_id=ADMINS, text_contains='download_book', state=None)
# async def chooseRegistry(call: CallbackQuery):
#     await call.message.answer(text='Выберите нужный реестр', reply_markup=registries(attribute='get'))
#     # избавляемся от часиков
#     await bot.answer_callback_query(call.id)


# скачивание рееста
@dp.callback_query_handler(user_id=ADMINS, text_contains='get_registry')
async def downloadRegistry(call: CallbackQuery):
    filename = call.data.split('_')[2]
    register = InputFile(path_or_bytesio=f'registries/{filename}')
    await call.message.answer_document(document=register)
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


# # выбор нужного реестра
# @dp.callback_query_handler(user_id=ADMINS, text_contains='set_active_registry')
# async def chooseNewActive(call: CallbackQuery):
#     await call.message.answer(text=f'Выберите нужный реестр\nТекущий активный - {get_active_registry()}',
#                               reply_markup=registries(attribute='set'))
#     # избавляемся от часиков
#     await bot.answer_callback_query(call.id)


# выбор инициатора
@dp.callback_query_handler(user_id=ADMINS, text_contains='download_files')
async def chooseIniciator(call: CallbackQuery):
    await call.message.answer(text='Выберите инициатора из списка', reply_markup=iniciators())
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(user_id=ADMINS, text_contains='iniciator_')
async def chooseFile(call: CallbackQuery):
    iniciator = call.data.split('_')[1]
    await call.message.answer(text='Выберите нужный файл', reply_markup=files(iniciator=iniciator))
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
