from aiogram.dispatcher.filters.state import StatesGroup, State


class CommentToOrder(StatesGroup):
    write_comment = State()
