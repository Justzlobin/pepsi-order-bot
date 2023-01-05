from aiogram.dispatcher import FSMContext
from states import UserRegisterName
import aiogram.utils.exceptions
from aiogram import Dispatcher
from create_bot import dp
from keyboards import *
from config import ADMIN


async def user_register(message: types.Message):
    await message.answer(text='register: ', reply_markup=user_register_kb())


async def user_register_name(query: types.CallbackQuery):
    await query.message.answer(text='Введіть імя')
    await UserRegisterName.user_choosing_name.set()


async def name_chosen(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_choosing_name'] = message.text
    print(data)

    await state.finish()
    await message.answer(
        text="дякую",
    )

def register_register_handlers(dp: Dispatcher):
    dp.register_message_handler(user_register, text='📋 Реєстрація')
    dp.register_callback_query_handler(user_register_name, cat_cb.filter(action='register_user_name'))
    dp.register_message_handler(name_chosen)
