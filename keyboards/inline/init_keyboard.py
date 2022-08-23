import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keys = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='План', callback_data='plan'),
            InlineKeyboardButton(text='Факт', callback_data='fact')
        ]
    ]
)

payment = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='100%', callback_data='payment_100%'),
            InlineKeyboardButton(text='50%', callback_data='payment_50%'),
            InlineKeyboardButton(text='Аванс', callback_data='payment_avans')
        ]
    ]
)

links = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Связаться с финансистом', callback_data='link_to_admin'),
        ],
        [
            InlineKeyboardButton(text='Мои завки', callback_data='get_my_payments'),
        ]
    ]
)
