from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher
from aiogram import types
from datadase import sqlite_db
from create_bot import dp
from keyboards import cat_cb, kb_custom


class CommentToOrder(StatesGroup):
    write_comment = State()


async def stop_comment(query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await query.answer(text='Дію скасовано!')
    await query.message.delete()


async def comment(query: types.CallbackQuery):
    await CommentToOrder.write_comment.set()
    await dp.bot.send_message(chat_id=query.message.chat.id,
                              text='Введіть примітку.\n'
                                   'Приклад:\n'
                                   '"Штрих" - штрихкоди\n'
                                   '"Серт" - сертифікат\n'
                                   '"ттн" - товаро-транспортна накладна\n')


async def write_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data_comment:
        data_comment['comment'] = message.text
        print(tuple(data_comment.values()))
    await sqlite_db.update_comment(message.from_user.id, state)
    await state.finish()
    await message.answer(text='Примітка збережена!', reply_markup=kb_custom)


def comment_order_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(comment, cat_cb.filter(action='comment'), state=None)
    dp.register_message_handler(write_comment, state=CommentToOrder.write_comment)
    dp.register_callback_query_handler(stop_comment, cat_cb.filter(action='stop_comment'), state='*')
