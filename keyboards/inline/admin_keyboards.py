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
            InlineKeyboardButton(text="далить книгу", callback_data='delete_book'),
        ],
[
            InlineKeyboardButton(text="Задать активный реестр", callback_data='set_active_registry'),
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
    for filename in os.listdir('registries'):
        keyboard.add(InlineKeyboardButton(text=filename, callback_data=f'{attribute}_registry_{filename}'))
    return keyboard
