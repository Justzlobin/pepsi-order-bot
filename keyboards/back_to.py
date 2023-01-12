from aiogram.types import InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData

Back_to = CallbackData('title', 'action')


def back_to_menu():
    return types.InlineKeyboardButton('Назад до меню', callback_data=Back_to.new(action='back_to_menu'))


def back_to_order():
    return types.InlineKeyboardButton('Назад', callback_data=Back_to.new(action='back_to_order'))
