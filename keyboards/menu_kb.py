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


def back_to_menu(designer=False):
    button = [
        [types.InlineKeyboardButton('Назад до меню', callback_data=Menu_KB.new(action='back_to_menu'))]
    ]
    if designer:
        return button
    else:
        return InlineKeyboardMarkup(inline_keyboard=button)


def combo_menu_kb():
    combo_buttons = []
    [combo_buttons.append(i) for i in menu_kb(designer=True) + back_to_menu(designer=True)]
    return InlineKeyboardMarkup(inline_keyboard=combo_buttons)
