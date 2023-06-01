from aiogram import Dispatcher
from keyboards.client_kb import *
from keyboards.menu_kb import *
from keyboards.back_to import *
from aiogram import types
from user_handlers.handler import edit_text, status, delete_message
from text.text_in_message import main_menu
from aiogram.utils import exceptions

async def price_cat(query: types.CallbackQuery):
    status.current_dialog_status_price(query.from_user.id)
    try:
        if status.dialog_status[query.from_user.id] == 'price':
            await edit_text(message=query.message, message_text='Категорії:',
                            reply_markup=cat_markup().add(back_to_menu_kb()))
        if status.dialog_status[query.from_user.id] == 'order':
            await edit_text(message=query.message, message_text='Категорії:',
                            reply_markup=cat_markup().add(back_to_order_kb()))
    except KeyError:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())
    print(f'user_name = {query.from_user.first_name} {query.from_user.last_name}')


async def price_brand(query: types.CallbackQuery, callback_data: dict):
    try:
        if status.dialog_status[query.from_user.id] == 'price':
            await edit_text(query.message, message_text='Бренди:',
                            reply_markup=brand_markup(callback_data['id']).add(
                                back_to_cat_from_brand_kb(), back_to_menu_kb()))
        if status.dialog_status[query.from_user.id] == 'order':
            await edit_text(query.message, message_text='Бренди:',
                            reply_markup=brand_markup(callback_data['id']).add(
                                back_to_cat_from_brand_kb(), back_to_order_kb()))
        if status.dialog_status[query.from_user.id] == 'admin':
            await edit_text(query.message, message_text='Бренди:',
                            reply_markup=brand_markup(callback_data['id']).add(
                                back_to_cat_from_brand_kb(), back_to_admin_menu_kb()))
    except KeyError:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())


async def price_tasty(query: types.CallbackQuery, callback_data: dict):
    brand_id = callback_data['id']
    try:

        if status.dialog_status[query.from_user.id] == 'price':
            await edit_text(query.message, message_text='Смаки:',
                            reply_markup=position_markup(brand_id, status.dialog_status[query.from_user.id]).row(
                                back_to_brand_from_tasty_kb(sqlite_db.select_cat_id(brand_id)), back_to_menu_kb()))
        if status.dialog_status[query.from_user.id] == 'order':
            await edit_text(query.message, message_text='Смаки:',
                            reply_markup=position_markup(brand_id, status.dialog_status[query.from_user.id]).row(
                                back_to_brand_from_tasty_kb(sqlite_db.select_cat_id(brand_id)), back_to_order_kb()))
        if status.dialog_status[query.from_user.id] == 'admin':
            await edit_text(query.message, message_text='Смаки:',
                            reply_markup=position_markup(brand_id, status.dialog_status[query.from_user.id]).row(
                                back_to_brand_from_tasty_kb(sqlite_db.select_cat_id(brand_id)),
                                back_to_admin_menu_kb()))
    except KeyError:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())


async def price_show_position(query: types.CallbackQuery, callback_data: dict):
    try:
        await query.message.delete()
    except exceptions.MessageToDeleteNotFound:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())
    dict_desc = sqlite_db.select_one_position(callback_data['id'])
    full_text = f"{dict_desc['brand_title']} {dict_desc['size']} {dict_desc['type']} " \
                f"{dict_desc['tasty_title']} {dict_desc['tasty_desc']}\n" \
                f"Ціна: {dict_desc['price']} грн.\n" \
                f"В ящику: {dict_desc['box_size']} ящ.\n" \
                f"Ціна за ящик: {round(dict_desc['price'] * dict_desc['box_size'], 2)} грн."
    try:
        message = await query.bot.send_photo(chat_id=query.message.chat.id,
                                             photo=types.InputFile(
                                                 fr"image/{callback_data['id']}.png"),
                                             caption=full_text,
                                             reply_markup=types.InlineKeyboardMarkup().add(
                                                 back_to_tasty_from_pos_kb(
                                                     callback_data['id'])))
    except FileNotFoundError:
        message = await query.bot.send_message(chat_id=query.message.chat.id,
                                               text=full_text,
                                               reply_markup=types.InlineKeyboardMarkup().add(
                                                   back_to_tasty_from_pos_kb(
                                                       callback_data['id'])))
    delete_message.change_message(user_id=query.from_user.id, message_id=message)


def register_price_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(price_cat, Menu_KB.filter(action='price'))
    dp.register_callback_query_handler(price_brand, Cat_KB.filter(action='from_cat_to_brand'))
    dp.register_callback_query_handler(price_tasty, Cat_KB.filter(action='from_brand_to_tasty'))
    dp.register_callback_query_handler(price_show_position, Cat_KB.filter(action='price_show_position'))
