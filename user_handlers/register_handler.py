from aiogram.dispatcher import FSMContext
from states import UserRegisterName
from aiogram import Dispatcher
from keyboards import *


async def stop_register(query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await query.bot.send_message(text='Головне меню', chat_id=query.message.chat.id, reply_markup=menu_kb())
    await query.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)


async def user_register(query: types.CallbackQuery):
    await query.bot.send_message(text='Ваші данні: ', reply_markup=user_register_kb(query.from_user.id),
                                 chat_id=query.message.chat.id)
    await query.message.delete()


async def user_register_name(query: types.CallbackQuery):
    await query.message.answer(text='Введіть ПІБ ФОП',
                               reply_markup=cancel_state(register=True))
    await UserRegisterName.user_enter_name.set()
    await query.message.delete()


async def user_register_address(query: types.CallbackQuery):
    await query.message.answer(text='Введіть адресу\n'
                                    'Приклад: м.Вінниця, Пирогова, 100',
                               reply_markup=cancel_state(register=True))
    await UserRegisterName.user_enter_address.set()
    await query.message.delete()


async def name_enter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_name'] = message.text
    if not user_db.check_user_for_registration(message.from_user.id):
        user_db.register_or_update_user_data(message.from_user.id, data['user_name'], name=True, register=True)
    user_db.register_or_update_user_data(message.from_user.id, data['user_name'], name=True)
    print(data)
    await state.finish()
    await message.answer(text='Ваші дані оновлені', reply_markup=menu_kb())
    await message.delete()


async def address_enter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_address'] = message.text
    if not user_db.check_user_for_registration(message.from_user.id):
        user_db.register_or_update_user_data(message.from_user.id, data['user_address'], address=True, register=True)
    user_db.register_or_update_user_data(message.from_user.id, data['user_address'], address=True)
    print(data)
    await state.finish()
    await message.answer(text='Ваші данні оновлені', reply_markup=menu_kb())
    await message.delete()


def register_register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(user_register, Menu_KB.filter(action='register'))
    dp.register_callback_query_handler(user_register_name, Cat_KB.filter(action='register_user_name'), state=None)
    dp.register_callback_query_handler(user_register_address, Cat_KB.filter(action='register_user_address'), state=None)
    dp.register_message_handler(name_enter, state=UserRegisterName.user_enter_name)
    dp.register_message_handler(address_enter, state=UserRegisterName.user_enter_address)
    dp.register_callback_query_handler(stop_register, Cat_KB.filter(action='stop_register'), state='*')
