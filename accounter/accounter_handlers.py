from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from user_handlers.handler import edit_text
from accounter_kb import accountant_keyboard


async def accountant_start(query: types.CallbackQuery):
    await edit_text(query.message, message_text='nothing', reply_markup=accountant_keyboard())


def register_accountant_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(accountant_start, Menu_KB.filter(action='accountant'))
