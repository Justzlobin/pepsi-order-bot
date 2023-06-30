from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datadase import sqlite_db, user_db
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from keyboards.menu_kb import Menu_KB
from datadase.admin_db import *


def accountant_keyboard():
    return [
        [types.InlineKeyboardButton('Додати операцію', callback_data=Menu_KB.new('add_operation'))],
        [types.InlineKeyboardButton('Статистика', callback_data=Menu_KB.new('stat'))]
    ]
