import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.tutor_callback import cancel_callback

tutorKeyboard_agree = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Весь документ', callback_data='tutor_agree_full'),
            InlineKeyboardButton(text='По отдельности', callback_data='tutor_agree_separately'),
            InlineKeyboardButton(text='По организации', callback_data='tutor_agree_organisation'),
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data=cancel_callback.new())
        ]
    ]
)

tutorKeyboard_question = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Написать', callback_data='tutor_question'),
            InlineKeyboardButton(text='Отмена', callback_data=cancel_callback.new())
        ]
    ]
)

tutorKeyboard_block = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='tutor_block'),
            InlineKeyboardButton(text='Отмена', callback_data=cancel_callback.new())
        ]
    ]
)
