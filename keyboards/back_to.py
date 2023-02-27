from aiogram import types
from aiogram.utils.callback_data import CallbackData

Back_to = CallbackData('title', 'action')
Back_to_id = CallbackData('title', 'id', 'action')


def back_to_menu_kb() -> object:
    return types.InlineKeyboardButton('🔙 Головне меню', callback_data=Back_to.new(action='back_to_menu'))


def back_to_order_menu_kb():
    return types.InlineKeyboardButton('🔙 Меню', callback_data=Back_to.new(action='back_to_order_menu'))


def back_to_admin_menu_kb():
    return types.InlineKeyboardButton('🔙 Адмін меню', callback_data=Back_to.new(action='back_to_admin_menu'))


def back_to_order_kb():
    return types.InlineKeyboardButton('🔙 Меню замовлення', callback_data=Back_to.new(action='back_to_start_order'))


def back_to_cat_from_brand_kb():
    return types.InlineKeyboardButton('⬅ Назад', callback_data=Back_to.new(
        action='back_to_cat_from_brand'))


def back_to_brand_from_tasty_kb(cat_id):
    return types.InlineKeyboardButton('⬅ Назад',
                                      callback_data=Back_to_id.new(id=cat_id,
                                                                   action='back_to_brand_from_tasty'))


def back_to_tasty_from_pos_kb(brand_id):
    return types.InlineKeyboardButton('⬅ Назад', callback_data=Back_to_id.new(id=brand_id,
                                                                              action='back_to_tasty_from_pos'))

