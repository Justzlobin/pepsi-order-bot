from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datadase import sqlite_db, user_db
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from keyboards.menu_kb import Menu_KB
from datadase.admin_db import *


def accountant_keyboard():
    buttons = [
        [types.InlineKeyboardButton('Додати операцію', callback_data=Menu_KB.new('add_operation'))],
        [types.InlineKeyboardButton('Детальна статистика', callback_data=Menu_KB.new('det_stat'))],
        [types.InlineKeyboardButton('Загальна статистика', callback_data=Menu_KB.new('gen_stat'))]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def cancel_add_record():
    buttons = [
        [types.InlineKeyboardButton('Cancel', callback_data=Menu_KB.new('cancel_record'))]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
