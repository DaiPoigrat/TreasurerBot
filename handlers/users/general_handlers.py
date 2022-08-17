# здесь прописываются хендлеры, общие для всех управляющих ролей

from aiogram.types import Message, ContentType, File, CallbackQuery, InputFile, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.inline import registries, cancelKeyboard, iniciators, files
from loader import dp, bot
from states.states import AdminStates
from utils.db_api.create_registry import get_date, create_book, set_active_registry, get_active_registry, readBuffer, \
    writeBuffer
import os


# считывание названия
@dp.callback_query_handler(user_id=ADMINS, text_contains='create_book', state=None)
async def setNewRegistryName(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text='Введите название рестра без расширения', reply_markup=cancelKeyboard)
    await AdminStates.EnterName.set()
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


# создание рееста
@dp.message_handler(user_id=ADMINS, state=AdminStates.EnterName)
async def createNewRegistry(message: Message, state: FSMContext):
    registry_name = message.text + '.xlsx'

    if registry_name in os.listdir('registries'):
        await message.answer(text='Реестр с таким названием уже существует.\nПожалуйста, введите другое!')
    else:
        create_book(name=registry_name)
        await state.reset_state(with_data=True)

        choice = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Да', callback_data=f'set_registry_{registry_name}'),
                    InlineKeyboardButton(text='Нет', callback_data='cancel'),
                ]
            ]
        )
        await message.answer(text='Реестр успешно создан!\nСделать его активным?', reply_markup=choice)


# делает реестр активным
@dp.callback_query_handler(user_id=ADMINS, text_contains='set_registry')
async def setActive(call: CallbackQuery):
    filename = call.data.split('_')[2]
    set_active_registry(new_active=filename)
    await call.message.answer(f'Активный реестр:\n{filename}')
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


# обработка команды отмена со всех клавиатур
@dp.callback_query_handler(text_contains='cancel')
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    # возврат пустой клавиатуры
    await call.message.edit_reply_markup(reply_markup=None)


# выбор нужного реестра
@dp.callback_query_handler(user_id=ADMINS, text_contains='download_book', state=None)
async def chooseRegistry(call: CallbackQuery):
    await call.message.answer(text='Выберите нужный реестр', reply_markup=registries(attribute='get'))
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


# скачивание рееста
@dp.callback_query_handler(user_id=ADMINS, text_contains='get_registry')
async def downloadRegistry(call: CallbackQuery):
    filename = call.data.split('_')[2]
    register = InputFile(path_or_bytesio=f'registries/{filename}')
    await call.message.answer_document(document=register)
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


# выбор нужного реестра
@dp.callback_query_handler(user_id=ADMINS, text_contains='set_active_registry')
async def chooseNewActive(call: CallbackQuery):
    await call.message.answer(text=f'Выберите нужный реестр\nТекущий активный - {get_active_registry()}',
                              reply_markup=registries(attribute='set'))
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


#
@dp.callback_query_handler(user_id=ADMINS, text_contains='download_files')
async def chooseIniciator(call: CallbackQuery):
    await call.message.answer(text='Выберите инициатора из списка', reply_markup=iniciators())
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(user_id=ADMINS, text_contains='iniciator_')
async def chooseFile(call: CallbackQuery):
    iniciator = call.data.split('_')[1]
    await call.message.answer(text='Выберите нужный файл', reply_markup=files(iniciator=iniciator))
    writeBuffer(inf=iniciator)
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(user_id=ADMINS, text_contains='download_file_')
async def downloadFile(call: CallbackQuery):
    filename = call.data.split('_')[2]
    iniciator = readBuffer()
    file = InputFile(path_or_bytesio=f'files/{iniciator}/{filename}')
    await call.message.answer_document(document=file)
    # избавляемся от часиков
    await bot.answer_callback_query(call.id)
