from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from create_bot import dp
from keyboards import *
from states.comment_states import CommentToOrder
from user_handlers.handler import del_mes, delete_message_from_dict


async def comment(query: types.CallbackQuery):
    await CommentToOrder.write_comment.set()
    message = await dp.bot.send_message(chat_id=query.message.chat.id,
                                        text='Введіть примітку.\n'
                                             'Приклад:\n'
                                             '<b>Дата доставки</b>\n'
                                             '<b>"Штрих"</b> - штрихкоди\n'
                                             '<b>"Серт"</b> - сертифікат\n'
                                             '<b>"ТТН"</b> - товаро-транспортна накладна\n',
                                        reply_markup=cancel_state())
    del_mes.add_message(chat_id=query.message.chat.id, message_id=message)
    await delete_message_from_dict(chat=query.message.chat.id)


async def stop_comment(query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    message = await query.bot.send_message(text='*Дію скасовано*\n'
                                                '1. Натисність <b>🛍️ Товари</b>, щоб почати формувати замовлення.\n'
                                                '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
                                                '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
                                           reply_markup=order_menu_kb(),
                                           chat_id=query.message.chat.id)
    del_mes.add_message(chat_id=query.message.chat.id, message_id=message)
    await delete_message_from_dict(chat=query.message.chat.id)


async def write_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data_comment:
        data_comment['comment'] = message.text
        print(tuple(data_comment.values()))
    await sqlite_db.update_comment(message.from_user.id, state)
    await state.finish()
    message = await message.answer(text='*Примітка збережена*\n'
                                        '1. Натисність <b>🛍️ Товари</b>, щоб почати формувати замовлення.\n'
                                        '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
                                        '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
                                   reply_markup=order_menu_kb())
    del_mes.add_message(chat_id=message.chat.id, message_id=message)
    await delete_message_from_dict(chat=message.chat.id)


def comment_order_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(comment, Cat_KB.filter(action='comment'), state=None)
    dp.register_callback_query_handler(stop_comment, Cat_KB.filter(action='stop_comment'), state='*')
    dp.register_message_handler(write_comment, state=CommentToOrder.write_comment)
    dp.register_callback_query_handler(stop_comment, Cat_KB.filter(action='stop_comment'), state='*')
