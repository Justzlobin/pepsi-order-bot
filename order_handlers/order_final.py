from aiogram import Dispatcher
from create_bot import dp
from keyboards import *
from user_handlers.handler import order_data


async def delete_from_order(query: types.CallbackQuery):
    sqlite_db.delete_from_order(order_data[f'{query.from_user.id}'])
    await query.answer(text='Замовлення скасовано!')
    await query.message.delete()


async def add_in_list_orders(query: types.CallbackQuery, callback_data: dict):
    await query.answer(text='Замовлення збережено!')
    sqlite_db.order_verification(callback_data['id'])
    await query.message.delete()
    await query.bot.send_message(text='Ще одне замовлення?)', chat_id=query.message.chat.id, reply_markup=menu_kb())


def register_order_final(dp: Dispatcher):
    dp.register_callback_query_handler(add_in_list_orders, cat_cb.filter(action='add_full_order'))
    dp.register_callback_query_handler(delete_from_order, cat_cb.filter(action='delete_from_order'))
