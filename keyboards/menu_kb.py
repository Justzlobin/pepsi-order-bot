from aiogram.types import InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData

Menu_KB = CallbackData('title', 'action')


def menu_kb():
    buttons = [
        [types.InlineKeyboardButton('💲 Замовлення', callback_data=Menu_KB.new(action='new_order'))],
        [types.InlineKeyboardButton('🗃 Історія замовлень', callback_data=Menu_KB.new(action='last_orders'))],
        [types.InlineKeyboardButton('📝 Реєстрація', callback_data=Menu_KB.new(action='register'))]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
