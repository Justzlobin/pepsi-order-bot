from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from datadase import sqlite_db, user_db
from aiogram import types
from aiogram.utils.callback_data import CallbackData

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
kb_menu_asort = KeyboardButton('🛍️ Асортимент')
kb_menu_register = KeyboardButton('📋 Реєстрація')
kb_menu_basket = KeyboardButton('🛒 Корзина')
kb_menu_new_custom = KeyboardButton('❎ Сформувати замовлення')
kb_last_order = KeyboardButton('📄 Останнє замовлення')
kb_order_settings = KeyboardButton('⚙ Налаштування')
kb_back_to_menu = KeyboardButton('🔙 Назад до меню')
kb_menu.add(kb_menu_new_custom, kb_last_order, kb_menu_register)

cat_cb = CallbackData('title', 'id', 'action')

kb_custom = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
kb_custom.add(kb_menu_asort, kb_menu_basket, kb_order_settings, kb_back_to_menu)

kb_menu_first_user = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
kb_menu_first_user.add(kb_menu_register)


def back_from_register_markup():
    back_from_register_kb = InlineKeyboardMarkup()
    back_from_register_kb.add(InlineKeyboardButton(
        'Відмінити',
        callback_data=cat_cb.new(id=1, action='back_to_menu_from_register')))
    return back_from_register_kb


def cat_markup():
    global cat_cb

    cat_cb_markup = InlineKeyboardMarkup()
    for cat_id, category_title in sqlite_db.select_all_categories():
        cat_cb_markup.add(InlineKeyboardButton(category_title, callback_data=cat_cb.new(id=cat_id,
                                                                                        action='cat->brand')))

    return cat_cb_markup


def brand_markup(cat_id):
    global cat_cb
    brand_cb_markup = InlineKeyboardMarkup()
    for brand_id, brand_title in sqlite_db.select_brand(cat_id):
        brand_cb_markup.add(
            InlineKeyboardButton(brand_title, callback_data=cat_cb.new(id=brand_id, action='brand->pos')))
    brand_cb_markup.add(InlineKeyboardButton('⬅ BACK', callback_data=cat_cb.new(id=int(cat_id),
                                                                                action='back_to_cat')))
    return brand_cb_markup


def position_markup(brand_id):
    global cat_cb

    position_cb_markup = InlineKeyboardMarkup()
    for position_id, position_title in sqlite_db.select_product(brand_id):
        position_cb_markup.add(InlineKeyboardButton(f'🍟 {position_title}', callback_data=cat_cb.new(
            id=position_id, action='position'
        )))

    position_cb_markup.add(InlineKeyboardButton('⬅ BACK', callback_data=cat_cb.new(id=sqlite_db.select_cat_id(brand_id),
                                                                                   action='cat->brand')))
    return position_cb_markup


def keyboard_order(order_id, user_id):
    global cat_cb

    keyboard_order_markup = InlineKeyboardMarkup()
    for pos_id, order_title in sqlite_db.list_from_order(order_id, user_id):
        keyboard_order_markup.add(InlineKeyboardButton(f'🛒 {order_title}',
                                                       callback_data=cat_cb.new(id=pos_id, action='position_order')))
    keyboard_order_markup.add(InlineKeyboardButton(f'✅ Пітдвердити замовення',
                                                   callback_data=cat_cb.new(id=order_id,
                                                                            action='add_full_order')))
    keyboard_order_markup.add(InlineKeyboardButton(f'❌ Скавувати замовлення',
                                                   callback_data=cat_cb.new(id=order_id,
                                                                            action='delete_from_order')))
    return keyboard_order_markup


def keyboard(pos_id, order=False, correct=False):
    list_commands = ['desc', 'zero', 'incr', 'finish']
    if order:
        list_commands = ['update_' + i for i in list_commands]
    if correct:
        list_commands = ['correct_' + i for i in list_commands]
    buttons = [
        [
            types.InlineKeyboardButton(text='➖',
                                       callback_data=cat_cb.new(id=pos_id, action=list_commands[0])),
            types.InlineKeyboardButton(text='⭕',
                                       callback_data=cat_cb.new(id=pos_id, action=list_commands[1])),
            types.InlineKeyboardButton(text='➕',
                                       callback_data=cat_cb.new(id=pos_id, action=list_commands[2]))
        ],
        [
            types.InlineKeyboardButton(text='Шт',
                                       callback_data=cat_cb.new(id=pos_id, action='multi')),
            types.InlineKeyboardButton(text='Ящ',
                                       callback_data=cat_cb.new(id=pos_id, action='box'))],
        [types.InlineKeyboardButton(text='Підтвердити',
                                    callback_data=cat_cb.new(id=pos_id, action=list_commands[3]))]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    keyboard.add(InlineKeyboardButton('⬅ BACK', callback_data=cat_cb.new(id=sqlite_db.select_brand_id(pos_id),
                                                                         action='back_to_position')))

    return keyboard


def keyboard_settings(order_id):
    buttons = [
        # [types.InlineKeyboardButton(text='Дата доставки',
        #                             callback_data=cat_cb.new(id=order_id, action='date_deliver'))],
        [types.InlineKeyboardButton(text='💰 Спосіб оплати',
                                    callback_data=cat_cb.new(id=order_id, action='payment'))],
        [types.InlineKeyboardButton(text='📝 Примітка',
                                    callback_data=cat_cb.new(id=order_id, action='comment'))]]
    keyboards = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboards


def chose_payment(user_id):
    buttons = [
        [types.InlineKeyboardButton(text='Готівкою',
                                    callback_data=cat_cb.new(id=user_id, action='cash'))],
        [types.InlineKeyboardButton(text='Банк',
                                    callback_data=cat_cb.new(id=user_id, action='bank'))]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def order_for_admin():
    order_to_admin_markup = InlineKeyboardMarkup()
    for i in sqlite_db.list_order_to_admin():
        order_to_admin_markup.add(InlineKeyboardButton(text=f'{i[0]} {i[1]} {i[2]} {i[3]}',
                                                       callback_data=cat_cb.new(id=i[0],
                                                                                action='order_admin')))
    return order_to_admin_markup


def order_for_user(user_id):
    order_to_user_markup = InlineKeyboardMarkup()
    for i in sqlite_db.list_order_to_user(user_id):
        order_to_user_markup.add(InlineKeyboardButton(text=f'{i[0]}  {sqlite_db.sum_order(i[1])}',
                                                      callback_data=cat_cb.new(id=i[1], action='order_user')))
    return order_to_user_markup


def order_state_kb(order_id):
    buttons = [
        [
            types.InlineKeyboardButton(text='Проведено',
                                       callback_data=cat_cb.new(id=order_id, action='order_agreed')),
            types.InlineKeyboardButton(text='Проведено (зі змінами)',
                                       callback_data=cat_cb.new(id=order_id, action='order_agreed_but'))
        ],
        [
            types.InlineKeyboardButton(text='Заблоковано (Дебіторка)',
                                       callback_data=cat_cb.new(id=order_id, action='order_blocked_debt')),
            types.InlineKeyboardButton(text='Заблоковано (Кредитний ліміт)',
                                       callback_data=cat_cb.new(id=order_id, action='order_blocked_limit'))
        ]
    ]
    order_state_kb_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return order_state_kb_markup


def order_update_user_kb(order_id):
    buttons = [
        [
            types.InlineKeyboardButton(text='Видалити',
                                       callback_data=cat_cb.new(id=order_id, action='order_delete')),
            types.InlineKeyboardButton(text='Згорнути',
                                       callback_data=cat_cb.new(id=order_id, action='order_close'))
        ]
    ]
    order_update_user_kb_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return order_update_user_kb_markup


def user_register_kb(user_id):
    if sqlite_db.user_exist():
        list_kb = user_db.select_name_and_address_from_users(user_id)
    else:
        list_kb = ('ПІБ ФОПа', 'АДРЕСА')
    buttons = [
        [
            types.InlineKeyboardButton(text=list_kb[0],
                                       callback_data=cat_cb.new(id=user_id, action='register_user_name')),
            types.InlineKeyboardButton(text=list_kb[1],
                                       callback_data=cat_cb.new(id=user_id, action='register_user_address'))
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


calendar_callback = CallbackData('simple_calendar', 'act', 'year', 'month', 'day')
