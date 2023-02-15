from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from keyboards import *
from states.admin_states import AdminAddPosition
from datadase.admin_db import *


async def start_add_position(query: types.CallbackQuery):
    await query.bot.send_message(text=f'Бренди:\n'
                                      f'{select_id_title_of_brand()}', chat_id=query.message.chat.id)
    await AdminAddPosition.brand.set()


async def admin_add_brand(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['brand'] = message.text
    await message.answer(text=f'{select_id_title_of_tasty(data_position["brand"])}')
    await AdminAddPosition.tasty.set()


async def admin_add_tasty(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['tasty'] = message.text
    await message.answer(text=f'{select_id_title_of_size()}')
    await AdminAddPosition.size.set()


async def admin_add_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['size'] = message.text
    await message.answer(text='Введіть ціну')
    await AdminAddPosition.price.set()


async def admin_add_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data_position:
        data_position['price'] = message.text
    if admin_add_new_position(data_position['brand'], data_position['tasty'], data_position['size'],
                              data_position['price']):
        await message.answer(text='Done')
    else:
        await message.answer(text='error')
    await state.finish()


def register_admin_add_pos_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_add_position, Admin_KB.filter(action='add_new_position'), state=None)
    dp.register_message_handler(admin_add_brand, state=AdminAddPosition.brand)
    dp.register_message_handler(admin_add_tasty, state=AdminAddPosition.tasty)
    dp.register_message_handler(admin_add_size, state=AdminAddPosition.size)
    dp.register_message_handler(admin_add_price, state=AdminAddPosition.price)
