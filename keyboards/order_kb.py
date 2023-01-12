from aiogram.types import InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from keyboards import back_to

order_kb = CallbackData('title', 'action')


def order_menu_kb():
    buttons = [
        [types.InlineKeyboardButton(text='Асортимент', callback_data=order_kb.new(action='assort'))],
        [types.InlineKeyboardButton(text='Корзина', callback_data=order_kb.new(action='basket'))],
        [types.InlineKeyboardButton(text='⚙ Налаштування', callback_data=order_kb.new(action='settings'))]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons).add(back_to.back_to_menu())
