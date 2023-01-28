from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminAddPosition(StatesGroup):
    brand = State()
    tasty = State()
    size = State()
    price = State()
    pos_id = State()
    in_stock = State()