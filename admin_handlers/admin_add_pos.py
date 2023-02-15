import types

from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from keyboards import *
from states.admin_states import AdminAddPosition
from user_handlers.handler import edit_text
from datadase.admin_db import select_id_title_of_category


async def start_add_position(query: types.CallbackQuery):
    await AdminAddPosition.category.set()
    await edit_text(message=query.message, message_text=f'Категорії:\n'
                                                        f'{select_id_title_of_category()}',
                    reply_markup=None)
    await AdminAddPosition.states.next()


async def admin_add_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['category'] = message.text
    await edit_text(message=message, message_text=f'Бренди:\n'
                                                  f'{select_id_title_of_brand()}', reply_markup=None)
    await AdminAddPosition.states.next()


def register_admin_add_pos_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_add_position, Admin_KB.filter(action='add_new_position'))
