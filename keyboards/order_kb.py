from aiogram.types import InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData

Order_KB = CallbackData('title', 'action')


def order_kb():
    buttons = [
        [types.InlineKeyboardButton(text='🛍 Товари', callback_data=Order_KB.new(action='order_product_list'))],
        [types.InlineKeyboardButton(text='🛒 Корзина', callback_data=Order_KB.new(action='basket'))],
        [types.InlineKeyboardButton(text='⚙ Налаштування', callback_data=Order_KB.new(action='settings'))]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def order_menu_kb():
    buttons = [
        [types.InlineKeyboardButton(text='Нове замовлення', callback_data=Order_KB.new(action='new_order'))],
        [types.InlineKeyboardButton(text='Останні замовлення', callback_data=Order_KB.new(action='last_order'))],
    ]

    return buttons