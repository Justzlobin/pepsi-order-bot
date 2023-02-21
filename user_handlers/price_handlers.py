from aiogram import Dispatcher
from keyboards.client_kb import *
from keyboards.back_to import *
from aiogram import types
from user_handlers.handler import edit_text


async def price_cat(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text='Category:', reply_markup=cat_markup().add(back_to_menu_kb()))


async def price_brand(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні бренди в категорії:',
                    reply_markup=brand_markup(callback_data['id']).add(
                        back_to_cat_from_brand_kb()))


async def price_tasty(query: types.CallbackQuery, callback_data: dict):
    print(callback_data['id'])
    print('price_tasty id')
    brand_id = callback_data['id']
    await edit_text(query.message, message_text='price_handler:',
                    reply_markup=position_markup(brand_id).add(
                        back_to_brand_from_tasty_kb(brand_id)))


def register_price_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(price_cat, Menu_KB.filter(action='price'))
    dp.register_callback_query_handler(price_brand, Cat_KB.filter(action='from_cat_to_brand'))
    dp.register_callback_query_handler(price_tasty, Cat_KB.filter(action='from_brand_to_tasty'))
