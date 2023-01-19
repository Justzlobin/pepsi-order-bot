from aiogram.utils import exceptions
from aiogram import Dispatcher
from create_bot import dp
from keyboards import *
from config import ADMIN
from user_handlers.handler import del_mes


async def admin_test(message: types.Message):
    chat = message.chat.id
    if message.from_user.id == int(ADMIN):
        sqlite_db.delete_not_verification()
        message = await message.answer(reply_markup=order_for_admin(), text='working')
    else:
        message = await message.answer('У вас немає доступу!')
    del_mes.add_message(chat, message)
    for message_in_dict in del_mes.chat_dict[chat][:-1]:
        try:
            await message_in_dict[0].delete()
        except exceptions.MessageToDeleteNotFound:
            pass


async def admin_test_kb(query: types.CallbackQuery, callback_data: dict):
    chat = query.message.chat.id
    try:
        message = await dp.bot.send_message(
            text=f'{sqlite_db.select_order_to_user_or_admin(callback_data["id"], admin=True)}',
            chat_id=query.message.chat.id,
            parse_mode='HTML', reply_markup=order_state_kb(callback_data['id']))
    except exceptions.MessageTextIsEmpty:
        message = await dp.bot.send_message(text='Замовлення пусте', chat_id=query.message.chat.id)
    del_mes.add_message(chat, message)
    for message_in_dict in del_mes.chat_dict[chat][:-1]:
        try:
            await message_in_dict[0].delete()
        except exceptions.MessageToDeleteNotFound:
            pass


async def order_status_agreed(query: types.CallbackQuery, callback_data: dict):
    sqlite_db.update_order_state(callback_data['id'], state='✅ Погоджено')
    await query.answer(text='статус змінено на ✅ Погоджено')
    await query.message.delete()


async def order_status_agreed_but(query: types.CallbackQuery, callback_data: dict):
    sqlite_db.update_order_state(callback_data['id'], state='✅ Погоджено (зі змінами)')
    await query.answer(text='статус змінено на ✅ Погоджено(зі змінами)')
    await query.message.delete()


async def order_status_blocked_debt(query: types.CallbackQuery, callback_data: dict):
    sqlite_db.update_order_state(callback_data['id'], state='❌ Заблоковано (Дебіт)')
    await query.answer(text='статус змінено на ❌ Заблоковано(дебіт)')
    await query.message.delete()


async def order_status_blocked_limit(query: types.CallbackQuery, callback_data: dict):
    sqlite_db.update_order_state(callback_data['id'], state='❌ Заблоковано (Ліміт)')
    await query.answer(text='статус змінено на ❌ Заблоковано(ліміт)')
    await query.message.delete()


async def order_delete(query: types.CallbackQuery, callback_data: dict):
    if sqlite_db.delete_order(callback_data['id']):
        await query.answer(text='Заявка видалена')
    else:
        await query.answer(text='Заявка вже проведена')
    await query.message.delete()


async def close_order_for_admin(query: types.CallbackQuery):
    await query.message.delete()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_test, text='admin')
    dp.register_callback_query_handler(admin_test_kb, Cat_KB.filter(action='order_admin'))
    dp.register_callback_query_handler(order_status_agreed, Cat_KB.filter(action='order_agreed'))
    dp.register_callback_query_handler(order_status_agreed_but, Cat_KB.filter(action='order_agreed_but'))
    dp.register_callback_query_handler(order_status_blocked_debt, Cat_KB.filter(action='order_blocked_debt'))
    dp.register_callback_query_handler(order_status_blocked_limit, Cat_KB.filter(action='order_blocked_limit'))
    dp.register_callback_query_handler(order_delete, Cat_KB.filter(action='order_delete'))
    dp.register_callback_query_handler(close_order_for_admin, Menu_KB.filter(action='close_admin'))
