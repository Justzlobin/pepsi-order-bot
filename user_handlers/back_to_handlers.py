from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from user_handlers.handler import edit_text


async def back_to_cat(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Categories:',
                    reply_markup=cat_markup().add(back_to_menu_kb()))


async def back_to_brand(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Brands:',
                    reply_markup=brand_markup(callback_data['id']).add(
                        back_to(back_to_cat_from_brand=callback_data['id'])))


async def back_to_main_menu(query: types.CallbackQuery):
    await edit_text(query.message, reply_markup=menu_kb(),
                    message_text='<b>PEPSIBOT</b>\n'
                                 'MAIN MENU')


async def back_to_order_menu(query: types.CallbackQuery):
    await edit_text(query.message,
                    message_text='ORDER MENU',
                    reply_markup=order_menu_kb().add(back_to_menu_kb()))


async def back_to_start_order(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text='ORDER_START',
                    reply_markup=order_kb().add(back_to_order_menu_kb()))


async def back_to_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(message=query.message, message_text='POSITIONS',
                    reply_markup=position_markup(callback_data['id']).add(
                        back_to(back_to_brand_from_pos=callback_data['id'])))


def register_back_to_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_main_menu, Back_to.filter(action='back_to_menu'))
    dp.register_callback_query_handler(back_to_cat, Back_to_id.filter(action='back_to_cat'))
    dp.register_callback_query_handler(back_to_brand, Back_to_id.filter(action='back_to_brand'))
    dp.register_callback_query_handler(back_to_order_menu, Back_to.filter(action='back_to_order_menu'))
    dp.register_callback_query_handler(back_to_start_order, Back_to.filter(action='back_to_start_order'))
    dp.register_callback_query_handler(back_to_position, Back_to_id.filter(action='back_to_pos'))
