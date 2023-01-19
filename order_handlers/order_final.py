from aiogram import Dispatcher
from keyboards import *
from user_handlers.handler import order_data, del_mes
from aiogram.utils import exceptions


async def delete_from_order(query: types.CallbackQuery):
    sqlite_db.delete_from_order(order_data[f'{query.from_user.id}'])
    chat = query.message.chat.id
    message = await query.bot.send_message(text='Замовлення скасовано!',
                                           reply_markup=menu_kb(),
                                           chat_id=query.message.chat.id)
    del_mes.add_message(chat, message)
    for message_in_dict in del_mes.chat_dict[chat][:-1]:
        try:
            await message_in_dict[0].delete()
        except exceptions.MessageToDeleteNotFound:
            pass


async def add_in_list_orders(query: types.CallbackQuery, callback_data: dict):
    await query.answer(text='Замовлення збережено!')
    sqlite_db.order_verification(callback_data['id'])
    chat = query.message.chat.id
    message = await query.bot.send_message(text='Ще одне замовлення?)', chat_id=query.message.chat.id,
                                           reply_markup=menu_kb())
    del_mes.add_message(chat, message)
    for message_in_dict in del_mes.chat_dict[chat][:-1]:
        try:
            await message_in_dict[0].delete()
        except exceptions.MessageToDeleteNotFound:
            pass


async def order_continue(query: types.CallbackQuery):
    chat = query.message.chat.id
    message = await query.bot.send_message(text='Меню замовлення:',
                                           chat_id=query.message.chat.id,
                                           reply_markup=order_menu_kb())
    del_mes.add_message(chat, message)
    for message_in_dict in del_mes.chat_dict[chat][:-1]:
        try:
            await message_in_dict[0].delete()
        except exceptions.MessageToDeleteNotFound:
            pass


def register_order_final(dp: Dispatcher):
    dp.register_callback_query_handler(add_in_list_orders, Cat_KB.filter(action='add_full_order'))
    dp.register_callback_query_handler(delete_from_order, Cat_KB.filter(action='delete_from_order'))
    dp.register_callback_query_handler(order_continue, Cat_KB.filter(action='continue_to_order'))
