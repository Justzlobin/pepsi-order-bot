import aiogram.utils.exceptions
from aiogram import Dispatcher
from create_bot import dp
from keyboards import *
from config import ADMIN
from datadase.admin_db import *
from user_handlers.handler import edit_text, status


async def admin_test(message: types.Message):
    await message.delete()
    status.current_dialog_status_admin(message.from_user.id)
    if message.from_user.id == int(ADMIN):
        await message.answer(text='Меню адміністратора',
                             reply_markup=admin_menu_kb().add(collapse_message_for_user_kb()))
    else:
        await message.answer('У вас немає доступу!')


async def admin_test_kb(query: types.CallbackQuery, callback_data: dict):
    try:
        await dp.bot.send_message(
            text=f'{sqlite_db.select_order_to_user_or_admin(callback_data["id"], admin=True)}',
            chat_id=query.message.chat.id,
            parse_mode='HTML', reply_markup=order_state_kb(callback_data['id']))
    except aiogram.utils.exceptions.MessageTextIsEmpty:
        await dp.bot.send_message(text='Замовлення пусте', chat_id=query.message.chat.id)


async def order_status_agreed(query: types.CallbackQuery, callback_data: dict):
    sqlite_db.update_order_state(callback_data['id'], state='✅ Погоджено')
    await query.bot.send_message(chat_id=user_db.get_user_id_to_order_id(callback_data['id']),
                                 text=f'{sqlite_db.select_order_to_user_or_admin(callback_data["id"])}',
                                 reply_markup=types.InlineKeyboardMarkup().add(collapse_message_for_user_kb()),
                                 parse_mode='HTML')
    await query.answer(text='статус змінено на ✅ Погоджено')
    await query.message.delete()


async def order_status_agreed_but(query: types.CallbackQuery, callback_data: dict):
    sqlite_db.update_order_state(callback_data['id'], state='✅ Погоджено (зі змінами)')
    await query.bot.send_message(chat_id=user_db.get_user_id_to_order_id(callback_data['id']),
                                 text=f'{sqlite_db.select_order_to_user_or_admin(callback_data["id"])}',
                                 reply_markup=types.InlineKeyboardMarkup().add(collapse_message_for_user_kb()),
                                 parse_mode='HTML')
    await query.answer(text='статус змінено на ✅ Погоджено(зі змінами)')
    await query.message.delete()


async def order_status_blocked_debt(query: types.CallbackQuery, callback_data: dict):
    sqlite_db.update_order_state(callback_data['id'], state='❌ Заблоковано (Дебіт)')
    await query.bot.send_message(chat_id=user_db.get_user_id_to_order_id(callback_data['id']),
                                 text=f'{sqlite_db.select_order_to_user_or_admin(callback_data["id"])}',
                                 reply_markup=types.InlineKeyboardMarkup().add(collapse_message_for_user_kb()),
                                 parse_mode='HTML')
    await query.answer(text='статус змінено на ❌ Заблоковано(дебіт)')
    await query.message.delete()


async def order_status_blocked_limit(query: types.CallbackQuery, callback_data: dict):
    sqlite_db.update_order_state(callback_data['id'], state='❌ Заблоковано (Ліміт)')
    await query.bot.send_message(chat_id=user_db.get_user_id_to_order_id(callback_data['id']),
                                 text=f'{sqlite_db.select_order_to_user_or_admin(callback_data["id"])}',
                                 reply_markup=types.InlineKeyboardMarkup().add(collapse_message_for_user_kb()),
                                 parse_mode='HTML')
    await query.answer(text='статус змінено на ❌ Заблоковано(ліміт)')
    await query.message.delete()


async def close_order_for_admin(query: types.CallbackQuery):
    await query.message.delete()


async def last_order_admin(query: types.CallbackQuery):
    await query.bot.send_message(text='Останні замовлення:', chat_id=query.message.chat.id,
                                 reply_markup=order_for_admin())


async def stock(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Category:',
                    reply_markup=cat_markup().add(back_to_admin_menu_kb()))


async def back_to_admin_menu(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Admin menu',
                    reply_markup=admin_menu_kb())


async def stock_brand(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Brands:',
                    reply_markup=brand_markup(callback_data['id']))


async def stock_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Positions:',
                    reply_markup=position_markup(callback_data['id'], status.dialog_status[query.from_user.id]).add(
                        back_to_brand_from_tasty_kb(sqlite_db.select_cat_id(callback_data['id']))))


async def stock_single_position(query: types.CallbackQuery, callback_data: dict):
    text = admin_select_one_position(callback_data['id'])
    full_text = f'{text[0]} {text[1]} {text[2]} {text[3]} {text[4]} {text[5]} {text[6]}'
    await edit_text(query.message, message_text=f'{full_text}\n', reply_markup=in_stock_kb(callback_data['id']))


async def in_stock_true(query: types.CallbackQuery, callback_data: dict):
    check_in_status(value=True, pos_id=callback_data['id'])
    await edit_text(query.message, message_text='Changed to TRUE',
                    reply_markup=position_markup(sqlite_db.select_brand_id(callback_data['id']),
                                                 status.dialog_status[query.from_user.id]).add(back_to_admin_menu_kb()))


async def in_stock_false(query: types.CallbackQuery, callback_data: dict):
    check_in_status(value=False, pos_id=callback_data['id'])
    await edit_text(query.message, message_text='Changed to FALSE',
                    reply_markup=position_markup(sqlite_db.select_brand_id(callback_data['id']),
                                                 status.dialog_status[query.from_user.id]).add(back_to_admin_menu_kb()))


async def collapse_message_for_user(query: types.CallbackQuery):
    await query.message.delete()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_test, text='admin')
    dp.register_callback_query_handler(order_status_agreed, Cat_KB.filter(action='order_agreed'))
    dp.register_callback_query_handler(order_status_agreed_but, Cat_KB.filter(action='order_agreed_but'))
    dp.register_callback_query_handler(order_status_blocked_debt, Cat_KB.filter(action='order_blocked_debt'))
    dp.register_callback_query_handler(order_status_blocked_limit, Cat_KB.filter(action='order_blocked_limit'))
    dp.register_callback_query_handler(close_order_for_admin, Menu_KB.filter(action='close_admin'))
    dp.register_callback_query_handler(last_order_admin, Admin_KB.filter(action='orders'))
    dp.register_callback_query_handler(stock, Admin_KB.filter(action='stock'))
    dp.register_callback_query_handler(back_to_admin_menu, Admin_KB.filter(action='back_to_admin_menu'))
    dp.register_callback_query_handler(stock_brand, Cat_KB.filter(action='admin_from_cat_to_brand'))
    dp.register_callback_query_handler(stock_position, Cat_KB.filter(action='admin_from_brand_to_pos'))
    dp.register_callback_query_handler(stock_single_position, Cat_KB.filter(action='admin_position'))
    dp.register_callback_query_handler(in_stock_true, Admin_cat_KB.filter(action='in_stock_true'))
    dp.register_callback_query_handler(in_stock_false, Admin_cat_KB.filter(action='in_stock_false'))
    dp.register_callback_query_handler(admin_test_kb, Cat_KB.filter(action='order_admin'))
    dp.register_callback_query_handler(collapse_message_for_user, Admin_KB.filter(action='collapse_message_for_user'))
