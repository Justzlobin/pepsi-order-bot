import types

from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from keyboards import *
from states.admin_states import AdminAddPosition
from user_handlers.handler import edit_text
from datadase.admin_db import select_id_title_from


async def start_add_position(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text=f'Категорії:\n'
                                                        f'{select_id_title_from("category")}',
                    reply_markup=None)
    await AdminAddPosition.category.set()


async def admin_add_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['category'] = message.text
    await message.answer(text=f'Бренди:\n'
                              f'{select_id_title_from("brand_cat")}', reply_markup=None)
    await AdminAddPosition.brand.set()


async def admin_add_brand(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['brand'] = message.text
    await message.answer(text=f'{select_id_title_from("size")}')
    await AdminAddPosition.size.set()


async def admin_add_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['size'] = message.text
    await message.answer(text=f'{select_id_title_from("tasty")}')
    await AdminAddPosition.tasty.set()


async def admin_add_tasty(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['tasty'] = message.text
    await message.answer(text='finish\n'
                              f'{data_position}')
    await state.finish()


def register_admin_add_pos_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_add_position, Admin_KB.filter(action='add_new_position'), state=None)
    dp.register_message_handler(admin_add_category, state=AdminAddPosition.category)
    dp.register_message_handler(admin_add_brand, state=AdminAddPosition.brand)
    dp.register_message_handler(admin_add_size, state=AdminAddPosition.size)
    dp.register_message_handler(admin_add_tasty, state=AdminAddPosition.tasty)
