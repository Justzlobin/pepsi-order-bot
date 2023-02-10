from aiogram import types
from aiogram.utils.callback_data import CallbackData

Back_to = CallbackData('title', 'action')


def back_to_menu():
    return types.InlineKeyboardButton('📂 Головне меню', callback_data=Back_to.new(action='back_to_menu'))


def back_to_order_menu():
    return types.InlineKeyboardButton('📝 Меню замовлення', callback_data=Back_to.new(action='back_to_order_menu'))


def back_to_admin_menu():
    return types.InlineKeyboardButton('admin меню', callback_data=Back_to.new(action='back_to_admin_menu'))
