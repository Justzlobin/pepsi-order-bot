from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram import Dispatcher
from datadase import sqlite_db
from keyboards import *


class UserRegister(StatesGroup):
    full_name = State()
    address = State()


async def cm_start(message: types.Message):
    await UserRegister.full_name.set()
    await message.reply("Введіть прізвище, ім'я, по-батькові ФОП", reply_markup=back_from_register_kb)


async def write_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text
        print(data)
    await UserRegister.next()
    await message.reply('І ще адресу доставки:\n Приклад: "м.Вінниця, Пирогова, 119"',
                        reply_markup=back_from_register_kb)


async def write_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
        print(data)
    await sqlite_db.add_user(state, message.from_user.id)
    await state.finish()
    await message.answer(text='Тепер можна робити замовлення', reply_markup=kb_menu)


async def fsc_close(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.answer(reply_markup=kb_menu, text='Ви повернулись в меню')



def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(cm_start, text='📋 Реєстрація', state=None)
    dp.register_message_handler(write_full_name, state=UserRegister.full_name)
    dp.register_message_handler(write_address, state=UserRegister.address)
    dp.register_callback_query_handler(fsc_close,
                                       back_from_register.filter(action='back_to_menu_from_register'))
