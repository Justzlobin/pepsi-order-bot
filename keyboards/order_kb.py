from aiogram.types import InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData

order_kb = CallbackData('title', 'action')


def order_inline_kb():
    buttons = [
        [types.InlineKeyboardButton(text='Асортимент', callback_data=order_kb.new(action='assort'))],
        [types.InlineKeyboardButton(text='Корзина', callback_data=order_kb.new(action='basket'))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
