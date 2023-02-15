import types

from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from keyboards import *
from states.admin_states import AdminAddPosition
from user_handlers.handler import edit_text
from datadase.admin_db import select_id_title_of_category


async def start_add_position(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text=f'Категорії:\n'
                                                        f'{select_id_title_of_category()}',
                    reply_markup=None)
    await AdminAddPosition.category.set()


async def admin_add_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['category'] = message.text
    await message.answer(text=f'Бренди:\n'
                              f'{select_id_title_of_brand()}', reply_markup=None)
    await AdminAddPosition.brand.set()


async def admin_add_brand(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['brand'] = message.text
    await message.answer(text='finish', reply_markup=None)
    print(data_position)
    await state.finish()


def register_admin_add_pos_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_add_position, Admin_KB.filter(action='add_new_position'), state=None)
    dp.register_message_handler(admin_add_category, state=AdminAddPosition.category)
    dp.register_message_handler(admin_add_brand, state=AdminAddPosition.brand)
