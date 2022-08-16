import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.accountant_callback import cancel_callback

accountantKeyboard_agree = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Весь документ', callback_data='accountant_agree_full'),
            InlineKeyboardButton(text='По отдельности', callback_data='accountant_agree_separately'),
            InlineKeyboardButton(text='По организации', callback_data='accountant_agree_organisation'),
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)

accountantKeyboard_question = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Написать', callback_data='accountant_question'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)

accountantKeyboard_block = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='accountant_block'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)
