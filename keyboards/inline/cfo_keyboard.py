import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.cfo_callback import cancel_callback

cfoKeyboard_to_excel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='download_book'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)

cfoKeyboard_agree = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Весь документ', callback_data='cfo_agree_full'),
            InlineKeyboardButton(text='По отдельности', callback_data='cfo_agree_separately'),
            InlineKeyboardButton(text='По организации', callback_data='cfo_agree_organisation'),
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)

cfoKeyboard_question = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Написать', callback_data='cfo_question'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)

cfoKeyboard_block = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='cfo_block'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)
