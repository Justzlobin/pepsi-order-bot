from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegisterName(StatesGroup):
    user_enter_name = State()
    user_enter_address = State()