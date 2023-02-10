from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from aiogram.utils import exceptions
from user_handlers.handler import edit_text


async def price_cat(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text='Category:', reply_markup=cat_markup())


async def price_position(query: types.CallbackQuery, callback_data: dict):
    text = sqlite_db.select_one_position(callback_data['id'])
    full_text = f'{text[0]} {text[1]} {text[2]} {text[3]} {text[4]}'
    await edit_text(message=query.message, message_text=full_text, reply_markup=back_to_menu())


def register_price_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(price_cat, Menu_KB.filter(action='price'))
    dp.register_callback_query_handler(price_position, Cat_KB.filter(action='price_position'))
