from aiogram import Dispatcher
from keyboards import *
from .handler import edit_text
from text.text_in_message import menu


async def view_order_for_user(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text=f'{sqlite_db.select_order_to_user_or_admin(callback_data["id"])}',
                    reply_markup=order_update_user_kb(callback_data['id']))


async def order_correct_user(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text=f'Ваше замовлення: <b>{sqlite_db.sum_order(callback_data["id"])}</b>',
                    reply_markup=keyboard_order(sqlite_db.select_last_order(query.from_user.id),
                                                user_id=query.message.from_user.id))


async def order_close_user(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Останні замовлення:',
                    reply_markup=order_for_user(query.from_user.id).add(back_to_order_menu_kb()))


async def order_delete(query: types.CallbackQuery, callback_data: dict):
    if sqlite_db.delete_order(callback_data['id']):
        await query.answer(text='Заявка видалена')
    else:
        await query.answer(text='Заявка вже проведена')
    await edit_text(message=query.message, message_text=menu, reply_markup=order_menu_kb().add(
        back_to_menu_kb()))


def register_update_order_handler(dp: Dispatcher):
    dp.register_callback_query_handler(view_order_for_user, Cat_KB.filter(action='order_user'))
    dp.register_callback_query_handler(order_correct_user, Cat_KB.filter(action='order_correct'))
    dp.register_callback_query_handler(order_close_user, Cat_KB.filter(action='order_close'))
    dp.register_callback_query_handler(order_delete, Cat_KB.filter(action='order_delete'))
