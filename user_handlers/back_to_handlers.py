from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from user_handlers.handler import edit_text, order, status, photo, delete_photo
from datadase.sqlite_db import select_cat_id


async def back_to_cat_from_brand(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Categories:',
                    reply_markup=cat_markup().add(back_to_order_kb()))


async def back_to_brand_from_tasty(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Brands:',
                    reply_markup=brand_markup(callback_data['id']).add(
                        back_to_cat_from_brand_kb()))


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


async def back_to_tasty_from_pos(query: types.CallbackQuery, callback_data: dict):
    # await delete_photo(query.message.chat.id)
    brand_id = sqlite_db.select_brand_id(callback_data['id'])
    await edit_text(message=query.message, message_text='POSITIONS',
                    reply_markup=position_markup(brand_id, status.dialog_status[query.from_user.id]).add(
                        back_to_brand_from_tasty_kb(select_cat_id(brand_id))))
    try:
        del order.order_dict[query.from_user.id][callback_data['id']]
    except KeyError:
        pass




def register_back_to_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_tasty_from_pos, Back_to_id.filter(action='back_to_tasty_from_pos'))
    dp.register_callback_query_handler(back_to_cat_from_brand, Back_to.filter(action='back_to_cat_from_brand'))
    dp.register_callback_query_handler(back_to_brand_from_tasty, Back_to_id.filter(action='back_to_brand_from_tasty'))
    dp.register_callback_query_handler(back_to_order_menu, Back_to.filter(action='back_to_order_menu'))
    dp.register_callback_query_handler(back_to_start_order, Back_to.filter(action='back_to_start_order'))
    dp.register_callback_query_handler(back_to_main_menu, Back_to.filter(action='back_to_menu'))
