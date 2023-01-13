from aiogram import Dispatcher
from create_bot import dp
from keyboards import *


async def show_assortment(query: types.CallbackQuery):
    await query.bot.send_message(text='Доступні категорії:',
                                 chat_id=query.message.chat.id,
                                 reply_markup=cat_markup(assortment=True))
    await query.message.delete()


async def assortment_back_to_cat(query: types.CallbackQuery):
    await query.bot.send_message(text='Доступні категорії:',
                              chat_id=query.message.chat.id,
                              reply_markup=cat_markup(assortment=True))
    await query.message.delete()

async def assortment_back_to_brand(query: types.CallbackQuery):
    await query.bot.send_message()


def register_assortment_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(show_assortment, Menu_KB.filter(action='assortment'))
    dp.register_callback_query_handler(assortment_back_to_cat, Cat_KB.filter(action='assortment_back_to_cat'))
