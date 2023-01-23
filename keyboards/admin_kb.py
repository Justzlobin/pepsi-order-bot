from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datadase import sqlite_db, user_db
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from keyboards import back_to

Admin_KB = CallbackData('title', 'action')


def admin_menu_kb():
    buttons = [
        [types.InlineKeyboardButton(text='Останні замовлення', callback_data=Admin_KB.new(action='orders'))],
        [types.InlineKeyboardButton(text='Склад', callback_data=Admin_KB.new(action='stock'))],
        [types.InlineKeyboardButton(text='Додати товар', callback_data=Admin_KB.new(action='add_new_position'))]
    ]
    admin_kb_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return admin_kb_markup.add(back_to.back_to_menu())