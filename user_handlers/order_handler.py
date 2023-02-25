from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from datadase.sqlite_db import save_order
from .handler import order, edit_text


async def order_basket_confirm(query: types.CallbackQuery):
    if order.order_dict[query.from_user.id]:
        save_order(user_id=query.from_user.id, order_dict=order.order_dict[query.from_user.id])
        await query.answer(text='Додано')
        await edit_text(message=query.message, message_text='ORDER MENU KB',
                        reply_markup=order_menu_kb().add(back_to_menu_kb()))
    else:
        await query.answer(text='Корзина пуста')
        await edit_text(message=query.message, message_text='ORDER MENU KB',
                        reply_markup=order_menu_kb().add(back_to_menu_kb()))


async def order_basket_cancel(query: types.CallbackQuery):
    del order.order_dict[query.from_user.id]
    await edit_text(message=query.message, message_text='MAIN MENU',
                    reply_markup=order_menu_kb())


def register_order_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(order_basket_confirm, Order_KB.filter(action='order_basket_confirm'))
    dp.register_callback_query_handler(order_basket_cancel, Order_KB.filter(action='order_basket_cancel'))
