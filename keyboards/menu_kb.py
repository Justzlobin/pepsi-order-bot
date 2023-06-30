from aiogram.types import InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from config import ADMIN

Menu_KB = CallbackData('title', 'action')


def menu_kb(user_id):
    buttons = [
        [types.InlineKeyboardButton('🧃 Прайс', callback_data=Menu_KB.new(action='price'))],
        [types.InlineKeyboardButton('🛒 Меню замовлень', callback_data=Menu_KB.new(action='order_menu'))],
        # [types.InlineKeyboardButton('🗃 Історія замовлень', callback_data=Menu_KB.new(action='last_orders'))],
    ]
    if str(user_id) == ADMIN:
        buttons.append([types.InlineKeyboardButton('Accounter', callback_data=Menu_KB.new(action='accountant'))])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def register_kb(button=False):
    if button:
        return types.InlineKeyboardButton('📝 Реєстрація', callback_data=Menu_KB.new(action='register'))
    else:
        buttons = [
            [types.InlineKeyboardButton('📝 Реєстрація', callback_data=Menu_KB.new(action='register'))]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
