from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminAddPosition(StatesGroup):
    category = State()
    brand = State()
    tasty = State()
    size = State()
    price = State()
    in_stock = State()
