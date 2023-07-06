from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from user_handlers.handler import edit_text
from aiogram.dispatcher import FSMContext
from accounter.accountant_db import accountant_add_record_in_db, sum_record
from accounter.accounter_other import AddRecordAccountant, det_stat_for_user, gen_stat_for_user
from accounter.accounter_kb import accountant_keyboard, cancel_add_record
from classes.delete import StateMessage
from keyboards.back_to import back_to_menu_kb

register_delete = StateMessage()


async def stop_record(query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await edit_text(query.message, message_text='main_menu',
                    reply_markup=accountant_keyboard())


async def accountant_start(query: types.CallbackQuery):
    await edit_text(query.message, message_text='nothing', reply_markup=accountant_keyboard().add(back_to_menu_kb()))


async def accountant_record_from_user(query: types.CallbackQuery):
    register_delete.add_message(query.message)
    await edit_text(query.message, message_text='Додайте операцію', reply_markup=cancel_add_record())
    await AddRecordAccountant.add_record.set()


async def accountant_add_record(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['record'] = message.text
    try:
        if accountant_add_record_in_db(data['record']):
            await edit_text(message=register_delete.message_dict['message'], message_text='Done!',
                            reply_markup=accountant_keyboard().add(back_to_menu_kb()))
        else:
            await edit_text(message=register_delete.message_dict['message'], message_text='Error!',
                            reply_markup=accountant_keyboard().add(back_to_menu_kb()))
    except:
        pass
    await state.finish()


async def det_stat_accountant(query: types.CallbackQuery):
    await edit_text(query.message, message_text=det_stat_for_user(sum_record()), reply_markup=accountant_keyboard())


async def gen_stat_accountant(query: types.CallbackQuery):
    await edit_text(query.message, message_text=gen_stat_for_user(sum_record()), reply_markup=accountant_keyboard())


def register_accountant_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(stop_record, Menu_KB.filter(action='cancel_record'), state='*')
    dp.register_callback_query_handler(accountant_start, Menu_KB.filter(action='accountant'))
    dp.register_callback_query_handler(det_stat_accountant, Menu_KB.filter(action='det_stat'))
    dp.register_callback_query_handler(gen_stat_accountant, Menu_KB.filter(action='gen_stat'))
    dp.register_callback_query_handler(accountant_record_from_user, Menu_KB.filter(action='add_operation'), state=None)
    dp.register_message_handler(accountant_add_record, state=AddRecordAccountant.add_record)
