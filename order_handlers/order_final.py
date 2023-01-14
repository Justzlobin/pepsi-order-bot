from aiogram import Dispatcher
from keyboards import *
from user_handlers.handler import order_data
from user_handlers.handler import delete_message


async def delete_from_order(query: types.CallbackQuery):
    sqlite_db.delete_from_order(order_data[f'{query.from_user.id}'])
    await query.bot.send_message(text='Замовлення скасовано!',
                                 reply_markup=menu_kb(),
                                 chat_id=query.message.chat.id)
    await delete_message.destr_photo()
    await query.message.delete()


async def add_in_list_orders(query: types.CallbackQuery, callback_data: dict):
    await query.answer(text='Замовлення збережено!')
    sqlite_db.order_verification(callback_data['id'])
    await query.message.delete()
    await delete_message.destr_photo()
    await query.bot.send_message(text='Ще одне замовлення?)', chat_id=query.message.chat.id, reply_markup=menu_kb())


async def order_continue(query: types.CallbackQuery):
    await query.message.delete()
    await delete_message.destr_photo()
    await query.bot.send_message(text='Меню замовлення:',
                                 chat_id=query.message.chat.id,
                                 reply_markup=order_menu_kb())


def register_order_final(dp: Dispatcher):
    dp.register_callback_query_handler(add_in_list_orders, Cat_KB.filter(action='add_full_order'))
    dp.register_callback_query_handler(delete_from_order, Cat_KB.filter(action='delete_from_order'))
    dp.register_callback_query_handler(order_continue, Cat_KB.filter(action='continue_to_order'))
