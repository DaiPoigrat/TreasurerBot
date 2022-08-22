import logging
import psycopg2
from data.config import DB_URI

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from utils.db_api.db_manage import get_users_id, get_files_id

# кнопка отмены
cancelKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)
# управление реестром
dataBaseKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Скачать книгу", callback_data='download_register'),
        ],
        [
            InlineKeyboardButton(text="Обновить данные", callback_data='update_register'),
        ],
        [
            InlineKeyboardButton(text='Скачать файлы', callback_data='download_files')
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data='cancel')
        ]
    ]
)
# закрытие канала общения
chatting_end = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Закончить общение', callback_data='chatting_end'),
        ]
    ]
)


def registries(attribute: str) -> InlineKeyboardMarkup:
    """
    attribute: get или set
    Возвращает клавиатуру, кнопки которой - названия всех реестров
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    try:
        for filename in os.listdir('registries'):
            keyboard.add(InlineKeyboardButton(text=filename, callback_data=f'{attribute}_registry_{filename}'))
    except:
        pass
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    return keyboard


def iniciators() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с инициаторами, когда-либо отправляющими файлы
    В качестве коллбека выступит id юзера
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    try:
        db_connection = psycopg2.connect(DB_URI, sslmode="require")
        db_object = db_connection.cursor()
        for iniciator in get_users_id():
            db_object.execute(
                f"SELECT payment_iniciator FROM register WHERE id = {iniciator[0]}"
            )

            result = db_object.fetchone()[0]
            keyboard.add(InlineKeyboardButton(text=f'{result}', callback_data=f'iniciator_{iniciator[0]}'))
    except Exception as err:
        logging.exception(err)
    finally:
        keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    return keyboard


def files(iniciator: str) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с файлами, отправленными данным инициатором
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    try:
        for file in get_files_id(user_id=iniciator):
            keyboard.add(InlineKeyboardButton(text=f'{file[0]}', callback_data=f'download_file_{file[1]}'))
    except Exception as err:
        logging.exception(err)
    finally:
        keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    return keyboard
