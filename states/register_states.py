from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegisterName(StatesGroup):
    user_choosing_name = State()
