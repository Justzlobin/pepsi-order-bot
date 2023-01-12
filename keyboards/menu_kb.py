from aiogram.types import InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData

Menu_KB = CallbackData('title', 'action')


def menu_kb(designer=False):
    buttons = [
        [types.InlineKeyboardButton('Замовлення', callback_data=Menu_KB.new(action='new_order'))],
        [types.InlineKeyboardButton('Історія замовлень', callback_data=Menu_KB.new(action='last_orders'))],
        [types.InlineKeyboardButton('Реєстрація', callback_data=Menu_KB.new(action='register'))]
    ]
    if designer:
        return buttons
    else:
        return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu():
    return [types.InlineKeyboardButton('Назад до меню', callback_data=Menu_KB.new(action='back_to_menu'))]
