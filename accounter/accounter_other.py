from aiogram.dispatcher.filters.state import StatesGroup, State


class AddRecordAccountant(StatesGroup):
    add_record = State()


def det_stat_for_user(stat):
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

    return '\n'.join(
        [f'{st[0]} {st[1]}' for st in set_plus.items()] and [f'{st[0]} {st[1]}' for st in set_minus.items()])


def gen_stat_for_user(stat):
    set_stat = {}

    for i in stat:
        if i[0] == '+':
            set_stat[i[2]] = 0
        if i[0] == '-':
            set_stat[i[2]] = 0

    for i in stat:
        if i[0] == '+':
            set_stat[i[2]] += i[1]
        if i[0] == '-':
            set_stat[i[2]] -= i[1]

    return '\n'.join([f'{st[0]} {st[1]}' for st in set_stat.items()])
