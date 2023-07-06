from aiogram.dispatcher.filters.state import StatesGroup, State


class AddRecordAccountant(StatesGroup):
    add_record = State()


def stat_for_user(stat):
    set_plus = {}
    set_minus = {}

    for i in stat:
        if i[0] == '+':
            set_plus[i[2]] = 0
        if i[0] == '-':
            set_minus[i[2]] = 0

    for i in stat:
        if i[0] == '+':
            set_plus[i[2]] += i[1]
        if i[0] == '-':
            set_minus[i[2]] -= i[1]

    return set_plus, set_minus
