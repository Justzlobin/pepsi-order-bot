from aiogram.dispatcher import FSMContext
from states import UserRegisterName
from aiogram import Dispatcher
from keyboards import *


async def stop_register(query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await query.answer(text='Дію скасовано!')
    await query.message.delete()


async def user_register(message: types.Message):
    await message.answer(text='Ваші данні: ', reply_markup=user_register_kb(message.from_user.id))


async def user_register_name(query: types.CallbackQuery):
    await query.message.answer(text='Введіть ПІБ ФОП',
                               reply_markup=cancel_state(register=True))
    await UserRegisterName.user_enter_name.set()


async def user_register_address(query: types.CallbackQuery):
    await query.message.answer(text='Введіть адресу\n'
                                    'Приклад: м.Вінниця, Пирогова, 100',
                               reply_markup=cancel_state(register=True))
    await UserRegisterName.user_enter_address.set()


async def name_enter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_name'] = message.text
    if not user_db.check_user_for_registration(message.from_user.id):
        user_db.register_or_update_user_data(message.from_user.id, data['user_name'], name=True, register=True)
    user_db.register_or_update_user_data(message.from_user.id, data['user_name'], name=True)
    print(data)
    await state.finish()
    await message.answer(text='Ваші дані оновлені', reply_markup=menu_kb())


async def address_enter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_address'] = message.text
    if not user_db.check_user_for_registration(message.from_user.id):
        user_db.register_or_update_user_data(message.from_user.id, data['user_address'], address=True, register=True)
    user_db.register_or_update_user_data(message.from_user.id, data['user_address'], address=True)
    print(data)
    await state.finish()
    await message.answer(text='Ваші данні оновлені', reply_markup=menu_kb())


def register_register_handlers(dp: Dispatcher):
    dp.register_message_handler(user_register, text='📋 Реєстрація')
    dp.register_callback_query_handler(user_register_name, Cat_KB.filter(action='register_user_name'), state=None)
    dp.register_callback_query_handler(user_register_address, Cat_KB.filter(action='register_user_address'), state=None)
    dp.register_message_handler(name_enter, state=UserRegisterName.user_enter_name)
    dp.register_message_handler(address_enter, state=UserRegisterName.user_enter_address)
    dp.register_callback_query_handler(stop_register, Cat_KB.filter(action='stop_register'), state='*')
