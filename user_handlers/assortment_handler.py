from aiogram import Dispatcher
from create_bot import dp
from keyboards import *


async def show_assortment(query: types.CallbackQuery, callback_data: dict):
    await query.bot.send_message(text='Доступні категорії:',
                                 chat_id=query.message.chat.id,
                                 reply_markup=brand_markup(callback_data['id']))


def register_assortment_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(show_assortment, Menu_KB.filter(action='assortment'))