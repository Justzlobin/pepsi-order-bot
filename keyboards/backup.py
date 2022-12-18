from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from datadase import sqlite_db
from aiogram import types
from aiogram.utils.callback_data import CallbackData

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
kb_menu_asort = KeyboardButton('🛍️ Асортимент')
kb_menu_register = KeyboardButton('📋 Реєстрація')
kb_menu.add(kb_menu_asort, kb_menu_register)


cat_cb = CallbackData('title', 'id', 'action')
brand_cb = CallbackData('brand', 'id', 'action')
position_cb = CallbackData('position', 'id', 'action')


def cat_markup():
    global cat_cb

    cat_cb_markup = InlineKeyboardMarkup()
    for cat_id, category_title in sqlite_db.select_all_categories():
        cat_cb_markup.add(InlineKeyboardButton(category_title, callback_data=cat_cb.new(id=cat_id, action='view')))
        print()

    return cat_cb_markup


def brand_markup(cat_id):
    global brand_cb
    brand_cb_markup = InlineKeyboardMarkup()
    for brand_id, brand_title in sqlite_db.select_brand(cat_id):
        brand_cb_markup.add(
            InlineKeyboardButton(brand_title, callback_data=brand_cb.new(id=brand_id, action='brand_view')))

    return brand_cb_markup


def position_markup(brand_id):
    global position_cb

    position_cb_markup = InlineKeyboardMarkup()
    for position_id, position_title in sqlite_db.select_product(brand_id):
        position_cb_markup.add(InlineKeyboardButton(f'🍟 {position_title}', callback_data=position_cb.new(
            id=position_id, action='tasty_view'
        )))
    position_cb_markup.add(InlineKeyboardButton('⬅ BACK', callback_data=position_cb.new(id=0, action='view')))
    return position_cb_markup


def keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text='-1',
                                       callback_data='num_decr'),
            types.InlineKeyboardButton(text='0',
                                       callback_data='num_zero'),
            types.InlineKeyboardButton(text='+1',
                                       callback_data='num_incr')
        ],
        [types.InlineKeyboardButton(text='підтвердити',
                                    callback_data='num_finish')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


"""FROM HANDLERS"""
async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(
        f'Вкажіть кількість: {new_value}',
        reply_markup=keyboard()
    )


async def cmd_numbers(message: types.Message):
    # photo = open('image/pepsi_05.png', 'rb')
    # await message.answer_photo(photo=photo)
    for pos in sqlite_db.select_all_position():
        await message.answer(f'{pos[0]} {pos[1]} {pos[2]} {pos[3]} {pos[4]}')
    await message.answer('Вкажіть число: 0', reply_markup=keyboard())
    user_data[message.from_user.id] = 0

async def callbacks_num(callback: types.CallbackQuery ):


    if action == "incr":
        user_data[callback.from_user.id] = user_value + 1
        await update_num_text(callback.message, user_value + 1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value - 1
        await update_num_text(callback.message, user_value - 1)
    elif action == 'zero':
        user_data[callback.from_user.id] = user_value - user_value
        await update_num_text(callback.message, 0)

    elif action == "finish":
        await callback.message.edit_text(f"Усього: {user_value}")
        user_data[callback.from_user.id] = user_value - user_value
        print(user_data)
        sqlite_db.add_position_in_order(callback.from_user.id, user_value, callback.message.chat)

    await callback.answer()

dp.register_callback_query_handler(callbacks_num)