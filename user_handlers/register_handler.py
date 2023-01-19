from aiogram.dispatcher import FSMContext
from states import UserRegisterName
from aiogram import Dispatcher
from keyboards import *
from delete.delete_message import UnMessage
from .handler import del_mes
from aiogram.utils import exceptions

delete_message = UnMessage()


async def stop_register(query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await query.bot.send_message(text='Головне меню', chat_id=query.message.chat.id, reply_markup=menu_kb())
    await delete_message.destr(query.message.chat.id).delete()


async def user_register(query: types.CallbackQuery):
    chat = query.message.chat.id
    message = await query.bot.send_message(text='Ваші данні: ',
                                           reply_markup=user_register_kb(
                                               query.from_user.id),
                                           chat_id=query.message.chat.id)
    del_mes.add_message(chat_id=chat, message_id=message)
    for message_in_dict in del_mes.chat_dict[chat][:-1]:
        try:
            await message_in_dict[0].delete()
        except exceptions.MessageToDeleteNotFound:
            pass


async def user_register_name(query: types.CallbackQuery):
    chat = query.message.chat.id
    message = await query.message.answer(text='Введіть ПІБ ФОП',
                                         reply_markup=cancel_state(register=True))
    await UserRegisterName.user_enter_name.set()
    del_mes.add_message(chat_id=chat,
                        message_id=message
                        )
    for message_in_dict in del_mes.chat_dict[chat][:-1]:
        try:
            await message_in_dict[0].delete()
        except exceptions.MessageToDeleteNotFound:
            pass


async def user_register_address(query: types.CallbackQuery):
    chat = query.message.chat.id
    message = await query.message.answer(text='Введіть адресу\n'
                                              'Приклад: м.Вінниця, Пирогова, 100',
                                         reply_markup=cancel_state(register=True))
    await UserRegisterName.user_enter_address.set()
    del_mes.add_message(chat_id=chat,
                        message_id=message
                        )
    for message_in_dict in del_mes.chat_dict[chat][:-1]:
        try:
            await message_in_dict[0].delete()
        except exceptions.MessageToDeleteNotFound:
            pass


async def name_enter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_name'] = message.text
    if not user_db.check_user_for_registration(message.from_user.id):
        user_db.register_or_update_user_data(message.from_user.id, data['user_name'], name=True, register=True)
    user_db.register_or_update_user_data(message.from_user.id, data['user_name'], name=True)
    await state.finish()
    chat = message.chat.id
    message = await message.answer(text='Ваші дані оновлені', reply_markup=menu_kb())
    del_mes.add_message(chat_id=chat,
                        message_id=message
                        )
    for message_in_dict in del_mes.chat_dict[chat][:-1]:
        try:
            await message_in_dict[0].delete()
        except exceptions.MessageToDeleteNotFound:
            pass


async def address_enter(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['user_address'] = message.text
    if not user_db.check_user_for_registration(message.from_user.id):
        user_db.register_or_update_user_data(message.from_user.id, data['user_address'], address=True, register=True)
    else:
        user_db.register_or_update_user_data(message.from_user.id, data['user_address'], address=True)
    await state.finish()
    chat = message.chat.id
    message = await message.answer(text='Ваші дані оновлені', reply_markup=menu_kb())
    del_mes.add_message(chat_id=chat,
                        message_id=message
                        )
    for message_in_dict in del_mes.chat_dict[chat][:-1]:
        try:
            await message_in_dict[0].delete()
        except exceptions.MessageToDeleteNotFound:
            pass


def register_register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(user_register, Menu_KB.filter(action='register'))
    dp.register_callback_query_handler(user_register_name, Cat_KB.filter(action='register_user_name'), state=None)
    dp.register_callback_query_handler(user_register_address, Cat_KB.filter(action='register_user_address'), state=None)
    dp.register_message_handler(name_enter, state=UserRegisterName.user_enter_name)
    dp.register_message_handler(address_enter, state=UserRegisterName.user_enter_address)
    dp.register_callback_query_handler(stop_register, Cat_KB.filter(action='stop_register'), state='*')
