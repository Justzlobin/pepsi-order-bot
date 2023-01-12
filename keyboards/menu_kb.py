from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData

Menu_KB = CallbackData('title', 'action')


def menu_kb():
    buttons = [
        [types.InlineKeyboardButton('Замовлення', action='new_order')],
        [types.InlineKeyboardButton('Історія замовлень', action='last_orders')],
        [types.InlineKeyboardButton('Реєстрація', action='register')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
