from aiogram.dispatcher import FSMContext
from states import UserRegisterName
from aiogram import Dispatcher
from keyboards import *
from .handler import edit_text
from classes.delete import StateMessage

register_delete = StateMessage()


async def stop_register(query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await edit_text(query.message, message_text='Головне меню:',
                    reply_markup=menu_kb())


async def user_register(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Ваші данні:',
                    reply_markup=user_register_kb(
                        query.from_user.id))


async def user_register_name(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Введіть ПІБ ФОП:',
                    reply_markup=cancel_state(register=True))
    register_delete.add_message(query.message)
    await UserRegisterName.user_enter_name.set()


async def user_register_address(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Введіть адресу:\n'
                                                'Приклад: м.Вінниця, Пирогова, 100',
                    reply_markup=cancel_state(register=True))
    register_delete.add_message(query.message)
    await UserRegisterName.user_enter_address.set()


async def user_register_title(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text='Введіть назву магазина:',
                    reply_markup=cancel_state(register=True))
    register_delete.add_message(query.message)
    await UserRegisterName.user_enter_title.set()


async def name_enter(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['user_name'] = message.text
    if not sqlite_db.user_exist(message.from_user.id):
        user_db.register_or_update_user_data(message.from_user.id, data['user_name'], name=True, register=True)
    else:
        user_db.register_or_update_user_data(message.from_user.id, data['user_name'], name=True)
    await state.finish()
    await edit_text(message=register_delete.message_dict['message'],
                    message_text='Головне меню:',
                    reply_markup=menu_kb())


async def address_enter(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['user_address'] = message.text
    if not sqlite_db.user_exist(message.from_user.id):
        user_db.register_or_update_user_data(message.from_user.id, data['user_address'], address=True, register=True)
    else:
        user_db.register_or_update_user_data(message.from_user.id, data['user_address'], address=True)
    print(data)
    await state.finish()
    await edit_text(message=register_delete.message_dict['message'],
                    message_text='*Дані оновлені*\n'
                                 '<b>PEPSIBOT</b>\n'
                                 'Натисніть:\n'
                                 '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
                                 'або сформувати замовлення. \n'
                                 '<b>🗃 Історія замовлень</b> - переглянути попередні замовлення.\n'
                                 '<b>📝 Реєстрація</b> - щоб розуміти кому відправляти замовлення.\n',
                    reply_markup=menu_kb())


async def title_enter(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['user_title'] = message.text
    if not sqlite_db.user_exist(message.from_user.id):
        user_db.register_or_update_user_data(message.from_user.id, data['user_title'], title=True, register=True)
    else:
        user_db.register_or_update_user_data(message.from_user.id, data['user_title'], title=True)
    await state.finish()
    await edit_text(message=register_delete.message_dict['message'],
                    message_text='*Дані оновлені*\n'
                                 '<b>PEPSIBOT</b>\n'
                                 'Натисніть:\n'
                                 '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
                                 'або сформувати замовлення. \n'
                                 '<b>🗃 Історія замовлень</b> - переглянути попередні замовлення.\n'
                                 '<b>📝 Реєстрація</b> - щоб розуміти кому відправляти замовлення.\n',
                    reply_markup=menu_kb())


def register_register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(user_register, Menu_KB.filter(action='register'))
    #
    dp.register_callback_query_handler(user_register_name, Cat_KB.filter(action='register_user_name'), state=None)
    dp.register_callback_query_handler(user_register_address, Cat_KB.filter(action='register_user_address'), state=None)
    dp.register_callback_query_handler(user_register_title, Cat_KB.filter(action='register_user_title'), state=None)
    #
    dp.register_message_handler(name_enter, state=UserRegisterName.user_enter_name)
    dp.register_message_handler(address_enter, state=UserRegisterName.user_enter_address)
    dp.register_message_handler(title_enter, state=UserRegisterName.user_enter_title)
    #
    dp.register_callback_query_handler(stop_register, Cat_KB.filter(action='stop_register'), state='*')
