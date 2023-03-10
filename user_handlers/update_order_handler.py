from aiogram import Dispatcher
from create_bot import dp
from keyboards import *
from .handler import del_mes, delete_message_from_dict


async def view_order_for_user(query: types.CallbackQuery, callback_data: dict):
    message = await dp.bot.send_message(text=f'{sqlite_db.select_order_to_user_or_admin(callback_data["id"])}',
                                        chat_id=query.message.chat.id,
                                        reply_markup=order_update_user_kb(callback_data['id']),
                                        parse_mode='HTML')
    del_mes.add_message(chat_id=query.message.chat.id, message_id=message)
    await delete_message_from_dict(chat=query.message.chat.id)


async def order_correct_user(query: types.CallbackQuery, callback_data: dict):
    await dp.bot.send_message(text=f'Ваше замовлення: <b>{sqlite_db.sum_order(callback_data["id"])}</b>',
                              chat_id=query.message.chat.id,
                              reply_markup=keyboard_order(sqlite_db.select_last_order(query.from_user.id),
                                                          query.from_user.id), parse_mode='HTML')


async def order_close_user(query: types.CallbackQuery):
    await query.message.delete()


def register_update_order_handler(dp: Dispatcher):
    dp.register_callback_query_handler(view_order_for_user, Cat_KB.filter(action='order_user'))
    dp.register_callback_query_handler(order_correct_user, Cat_KB.filter(action='order_correct'))
    dp.register_callback_query_handler(order_close_user, Cat_KB.filter(action='order_close'))
