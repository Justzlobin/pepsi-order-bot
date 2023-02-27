from aiogram.types import InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData

Order_KB = CallbackData('title', 'action')


def order_kb():
    buttons = [
        [types.InlineKeyboardButton(text='🛍 Товари', callback_data=Order_KB.new(action='order_product_list'))],
        [types.InlineKeyboardButton(text='🛒 Корзина', callback_data=Order_KB.new(action='order_basket'))],
        [types.InlineKeyboardButton(text='⚙ Налаштування', callback_data=Order_KB.new(action='order_settings'))]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def order_menu_kb():
    buttons = [
        [types.InlineKeyboardButton(text='📝 Нове замовлення', callback_data=Order_KB.new(action='new_order'))],
        [types.InlineKeyboardButton(text='🗃 Історія замовлень', callback_data=Order_KB.new(action='last_order'))],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def order_basket_kb():
    buttons = [
        [types.InlineKeyboardButton(text='✅ Підтвердити', callback_data=Order_KB.new(action='order_basket_confirm'))],
        [types.InlineKeyboardButton(text='🛑 Скасувати', callback_data=Order_KB.new(action='order_basket_cancel'))],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def keyboard_settings():
    buttons = [
        # [types.InlineKeyboardButton(text='Дата доставки',
        #                             callback_data=cat_cb.new(id=order_id, action='date_deliver'))],
        [types.InlineKeyboardButton(text='💰 Спосіб оплати',
                                    callback_data=Order_KB.new(action='payment'))],
        [types.InlineKeyboardButton(text='💬 Примітка',
                                    callback_data=Order_KB.new(action='comment'))]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def chose_payment():
    buttons = [
        [types.InlineKeyboardButton(text='💰 Готівкою',
                                    callback_data=Order_KB.new(action='cash'))],
        [types.InlineKeyboardButton(text='💳 Банк',
                                    callback_data=Order_KB.new(action='bank'))]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)