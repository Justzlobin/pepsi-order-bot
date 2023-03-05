from aiogram import Dispatcher
from keyboards import *
from user_handlers.handler import edit_text, order
from text.text_in_message import menu_order


async def calendar_prev_year(query: types.CallbackQuery, callback_data: dict):
    await edit_text(message=query.message, message_text='prev year',
                    reply_markup=start_calendar(year=callback_data['year'], month=callback_data['month']))


def register_calendar_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(calendar_prev_year, calendar_callback.filter(act='PREV-YEAR'))
