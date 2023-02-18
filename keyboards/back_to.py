from aiogram import types
from aiogram.utils.callback_data import CallbackData
from datadase.sqlite_db import select_cat_id, select_brand_id

Back_to = CallbackData('title', 'action')
Back_to_id = CallbackData('title', 'id', 'action')


def back_to_menu_kb():
    return types.InlineKeyboardButton('MAIN MENU', callback_data=Back_to.new(action='back_to_menu'))


def back_to_order_menu_kb():
    return types.InlineKeyboardButton('ORDER_MENU', callback_data=Back_to.new(action='back_to_order_menu'))


def back_to_admin_menu_kb():
    return types.InlineKeyboardButton('ADMIN MENU', callback_data=Back_to.new(action='back_to_admin_menu'))


def back_to_order_kb():
    return types.InlineKeyboardButton('ORDER_START', callback_data=Back_to.new(action='back_to_start_order'))


def back_to(back_to_cat_from_brand=None, back_to_brand_from_pos=None, back_to_pos=None):
    if back_to_cat_from_brand:
        return types.InlineKeyboardButton('⬅ Назад', callback_data=Back_to_id.new(id=int(back_to_cat_from_brand),
                                                                                  action='back_to_cat'))
    elif back_to_brand_from_pos:
        return types.InlineKeyboardButton('⬅ Назад', callback_data=Back_to.new(id=select_cat_id(back_to_brand_from_pos),
                                                                               action='back_to_brand'))
    elif back_to_pos:
        return types.InlineKeyboardButton('⬅ Назад', callback_data=Back_to_id.new(id=select_brand_id(back_to_pos),
                                                                                  action='back_to_pos'))
