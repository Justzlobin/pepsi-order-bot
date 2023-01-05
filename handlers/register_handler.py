import types

from aiogram.dispatcher import FSMContext
from states import UserRegisterName
import aiogram.utils.exceptions
from aiogram import Dispatcher
from create_bot import dp
from keyboards import *
from config import ADMIN


async def user_register(message: types.Message):
    await message.answer(text='register: ', reply_markup=user_register_kb())


# async def user_register_name(query: types.CallbackQuery, state: FSMContext):
#     await query.message.answer(text='Введіть імя')
#     await state.set_state(UserRegisterName.user_choosing_name)


def register_register_handlers(dp: Dispatcher):
    dp.register_message_handler(user_register, text='📋 Реєстрація')