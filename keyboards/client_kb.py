from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datadase import sqlite_db, user_db
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from keyboards.menu_kb import Menu_KB
from datadase.admin_db import *

Cat_KB = CallbackData('title', 'id', 'action')


def cat_markup():
    action = 'from_cat_to_brand'
    cat_kb_markup = InlineKeyboardMarkup()
    for cat_id, category_title in sqlite_db.select_all_categories():
        cat_kb_markup.add(InlineKeyboardButton(category_title, callback_data=Cat_KB.new(id=cat_id,
                                                                                        action=action)))
    return cat_kb_markup


def brand_markup(cat_id):
    brand_cb_markup = InlineKeyboardMarkup()

    for brand_id, brand_title in sqlite_db.select_brand(cat_id):
        brand_cb_markup.add(
            InlineKeyboardButton(brand_title, callback_data=Cat_KB.new(id=brand_id, action='from_brand_to_tasty')))

    return brand_cb_markup


def position_markup(brand_id, status):
    position_cb_markup = InlineKeyboardMarkup()
    if status == 'order':
        action = 'position'
        list_pos = sqlite_db.select_product(brand_id)
        for position_id, position_title in list_pos:
            position_cb_markup.add(InlineKeyboardButton(f'{position_title}', callback_data=Cat_KB.new(
                id=position_id, action=action
            )))

    if status == 'admin':
        action = 'admin_position'
        list_pos = admin_select_product(brand_id)
        for position_id, position_title in list_pos:
            position_cb_markup.add(InlineKeyboardButton(f'{position_title}', callback_data=Cat_KB.new(
                id=position_id, action=action
            )))

    if status == 'price':
        action = 'price_show_position'
        list_pos = sqlite_db.select_product(brand_id)
        for position_id, position_title in list_pos:
            position_cb_markup.add(InlineKeyboardButton(f'{position_title}', callback_data=Cat_KB.new(
                id=position_id, action=action
            )))

    return position_cb_markup


def keyboard_order(order_id, user_id):
    keyboard_order_markup = InlineKeyboardMarkup()
    for pos_id, order_title in sqlite_db.list_from_order(order_id, user_id):
        keyboard_order_markup.add(InlineKeyboardButton(f'🛒 {order_title}',
                                                       callback_data=Cat_KB.new(id=pos_id, action='position_order')))
    keyboard_order_markup.add(InlineKeyboardButton(f'✅ Пітдвердити замовення',
                                                   callback_data=Cat_KB.new(id=order_id,
                                                                            action='add_full_order')))
    keyboard_order_markup.add(InlineKeyboardButton(f'❌ Скавувати замовлення',
                                                   callback_data=Cat_KB.new(id=order_id,
                                                                            action='delete_from_order')))
    keyboard_order_markup.add(InlineKeyboardButton(f'📝 Продовжити замовлення',
                                                   callback_data=Cat_KB.new(id=order_id,
                                                                            action='continue_to_order')))
    return keyboard_order_markup


def keyboard(pos_id, order=False):
    list_commands = ['desc', 'zero', 'incr', 'finish']
    if order:
        list_commands = ['update_' + i for i in list_commands]
    buttons = [
        [
            types.InlineKeyboardButton(text='➖',
                                       callback_data=Cat_KB.new(id=pos_id, action=list_commands[0])),
            types.InlineKeyboardButton(text='⭕',
                                       callback_data=Cat_KB.new(id=pos_id, action=list_commands[1])),
            types.InlineKeyboardButton(text='➕',
                                       callback_data=Cat_KB.new(id=pos_id, action=list_commands[2]))
        ],
        [
            types.InlineKeyboardButton(text='Шт',
                                       callback_data=Cat_KB.new(id=pos_id, action='multi')),
            types.InlineKeyboardButton(text='Ящ',
                                       callback_data=Cat_KB.new(id=pos_id, action='box'))],
        [types.InlineKeyboardButton(text='Підтвердити',
                                    callback_data=Cat_KB.new(id=pos_id, action=list_commands[3]))]
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def order_for_admin():
    order_to_admin_markup = InlineKeyboardMarkup()
    for i in sqlite_db.list_order_to_admin():
        order_to_admin_markup.add(InlineKeyboardButton(text=f'{i[0]} {i[1]} {i[2]} {i[3]}',
                                                       callback_data=Cat_KB.new(id=i[0],
                                                                                action='order_admin')))
    order_to_admin_markup.add(InlineKeyboardButton(text='Згорнути', callback_data=Menu_KB.new(action='close_admin')))
    return order_to_admin_markup


def order_for_user(user_id):
    order_to_user_markup = InlineKeyboardMarkup()
    for i in sqlite_db.list_order_for_user(user_id):
        order_to_user_markup.add(InlineKeyboardButton(text=f'{i[0]} - {i[2]}',
                                                      callback_data=Cat_KB.new(id=i[1], action='order_user')))
    return order_to_user_markup


def order_state_kb(order_id):
    buttons = [
        [
            types.InlineKeyboardButton(text='✅ Проведено',
                                       callback_data=Cat_KB.new(id=order_id, action='order_agreed')),
            types.InlineKeyboardButton(text='✅ Проведено (зі змінами)',
                                       callback_data=Cat_KB.new(id=order_id, action='order_agreed_but'))
        ],
        [
            types.InlineKeyboardButton(text='❌ Заблоковано (Дебіторка)',
                                       callback_data=Cat_KB.new(id=order_id, action='order_blocked_debt')),
            types.InlineKeyboardButton(text='❌ Заблоковано (Кредитний ліміт)',
                                       callback_data=Cat_KB.new(id=order_id, action='order_blocked_limit'))
        ]
    ]
    order_state_kb_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return order_state_kb_markup


def order_update_user_kb(order_id):
    buttons = [
        [
            types.InlineKeyboardButton(text='Видалити',
                                       callback_data=Cat_KB.new(id=order_id, action='order_delete')),
            types.InlineKeyboardButton(text='Згорнути',
                                       callback_data=Cat_KB.new(id=order_id, action='order_close'))
        ]
    ]
    order_update_user_kb_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return order_update_user_kb_markup


def user_register_kb(user_id):
    if sqlite_db.user_exist(user_id):
        list_kb = user_db.select_name_address_title_from_users(user_id)[0]
    else:
        list_kb = ('ПІБ ФОПа', 'АДРЕСА', 'НАЗВА ТТ')
    buttons = [
        [
            types.InlineKeyboardButton(text=list_kb[0],
                                       callback_data=Cat_KB.new(id=user_id, action='register_user_name'))
        ],
        [types.InlineKeyboardButton(text=list_kb[1],
                                    callback_data=Cat_KB.new(id=user_id, action='register_user_address'))
         ],
        [
            types.InlineKeyboardButton(text=list_kb[2],
                                       callback_data=Cat_KB.new(id=user_id, action='register_user_title'))
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def cancel_state(register=False):
    action = 'stop_register' if register else 'stop_comment'
    button = [
        [types.InlineKeyboardButton(text='🛑 Відмінити', callback_data=Cat_KB.new(id=1, action=action))]
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=button)


calendar_callback = CallbackData('simple_calendar', 'act', 'year', 'month', 'day')
