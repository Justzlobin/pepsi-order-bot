from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from datadase.sqlite_db import save_order
from .handler import order, edit_text
from text.text_in_message import menu, menu_order


async def order_basket_confirm(query: types.CallbackQuery):
    save_order(user_id=query.from_user.id, order=order)
    await query.answer(text='Додано')
    await edit_text(message=query.message, message_text=menu,
                    reply_markup=order_menu_kb().add(back_to_menu_kb()))


async def order_basket_cancel(query: types.CallbackQuery):
    try:
        del order.order_dict[query.from_user.id]
    except KeyError:
        pass
    await edit_text(message=query.message, message_text=menu,
                    reply_markup=order_menu_kb().add(back_to_menu_kb()))


async def next_move_in_order_yes(query: types.CallbackQuery):
    try:
        del order.order_dict[query.from_user.id]
    except KeyError:
        pass
    await edit_text(message=query.message, message_text=menu, reply_markup=order_menu_kb().add(back_to_menu_kb()))


async def next_move_in_order_no(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text=menu_order,
                    reply_markup=order_kb().add(back_to_order_menu_kb()))


def register_order_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(order_basket_confirm, Order_KB.filter(action='order_basket_confirm'))
    dp.register_callback_query_handler(order_basket_cancel, Order_KB.filter(action='order_basket_cancel'))
    dp.register_callback_query_handler(next_move_in_order_yes, Order_KB.filter(action='next_move_in_order_yes'))
    dp.register_callback_query_handler(next_move_in_order_no, Order_KB.filter(action='next_move_in_order_no'))
