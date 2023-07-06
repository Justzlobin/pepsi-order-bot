from aiogram.dispatcher.filters.state import StatesGroup, State


class AddRecordAccountant(StatesGroup):
    add_record = State()


def stat_for_user(stat):
    positive = []
    negative = []
    set_desc = {}
    for i in stat:
        if i[0] == '+':
            positive.append((i[1], i[2]))
            set_desc[i[2]] = 0
            for a in positive:
                set_desc[i[2]] += i[1]
        if i[0] == '-':
            negative.append((i[1], i[2]))
            set_desc[i[2]] = 0
            for a in negative:
                set_desc[i[2]] -= i[1]

    return set_desc