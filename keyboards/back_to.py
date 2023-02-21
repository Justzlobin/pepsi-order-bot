from aiogram import types
from aiogram.utils.callback_data import CallbackData

Back_to = CallbackData('title', 'action')
Back_to_id = CallbackData('title', 'id', 'action')


def back_to_menu_kb() -> object:
    return types.InlineKeyboardButton('MAIN MENU', callback_data=Back_to.new(action='back_to_menu'))


def back_to_order_menu_kb():
    return types.InlineKeyboardButton('ORDER_MENU', callback_data=Back_to.new(action='back_to_order_menu'))


def back_to_admin_menu_kb():
    return types.InlineKeyboardButton('ADMIN MENU', callback_data=Back_to.new(action='back_to_admin_menu'))


def back_to_order_kb():
    return types.InlineKeyboardButton('ORDER_START', callback_data=Back_to.new(action='back_to_start_order'))


def back_to_cat_from_brand():
    return types.InlineKeyboardButton('⬅ Назад', callback_data=Back_to.new(
        action='back_to_cat_from_brand'))


def back_to_brand_from_tasty(cat_id):
    return types.InlineKeyboardButton('⬅ Назад',
                                      callback_data=Back_to_id.new(id=cat_id,
                                                                   action='back_to_brand_from_tasty'))


def back_to_tasty_from_pos(brand_id):
    return types.InlineKeyboardButton('⬅ Назад', callback_data=Back_to_id.new(id=brand_id,
                                                                              action='back_to_tasty_from_pos'))

