import typing

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

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
            InlineKeyboardButton(text="Создать книгу", callback_data='create_book'),
            InlineKeyboardButton(text="Скачать книгу", callback_data='download_book'),
        ],
        [
            InlineKeyboardButton(text="Задать активный реестр", callback_data='set_active_registry'),
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
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    try:
        for iniciator in os.listdir('files'):
            keyboard.add(InlineKeyboardButton(text=f'{iniciator}', callback_data=f'iniciator_{iniciator}'))
    except:
        pass
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    return keyboard


def files(iniciator: str) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с файлами, отправленными данным инициатором
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    try:
        for filename in os.listdir(f'files/{iniciator}'):
            keyboard.add(InlineKeyboardButton(text=f'{filename}', callback_data=f'download_file_{filename}'))
    except:
        pass
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    return keyboard
