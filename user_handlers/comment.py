from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from keyboards import *
from states.comment_states import CommentToOrder
from user_handlers.handler import edit_text, order, status
from text.text_in_message import menu_order, main_menu

comment_message = {}


async def comment(query: types.CallbackQuery):
    await CommentToOrder.write_comment.set()
    try:
        await edit_text(query.message,
                        message_text='Введіть примітку.\n'
                                     'Приклад:\n'
                                     '<b>Дата доставки</b>\n'
                                     '<b>"Штрих"</b> - штрихкоди\n'
                                     '<b>"Серт"</b> - сертифікат\n'
                                     '<b>"ТТН"</b> - товаро-транспортна накладна\n',
                        reply_markup=cancel_state(status=status.dialog_status[query.from_user.id]))
    except KeyError:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb(query.from_user.id))
    comment_message['message'] = query.message
    print(comment_message)


async def stop_comment(query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await edit_text(query.message, message_text=menu_order,
                    reply_markup=order_kb().add(back_to_order_menu_kb()))


async def write_comment(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data_comment:
        data_comment['comment'] = message.text
        print(tuple(data_comment.values()))
    try:
        order.add_comment(user_id=message.from_user.id, comment=data_comment['comment'])
    except KeyError:
        await edit_text(message=message, message_text=main_menu, reply_markup=menu_kb(query.from_user.id))
    await state.finish()
    await edit_text(message=comment_message['message'],
                    message_text=menu_order,
                    reply_markup=order_kb().add(back_to_order_menu_kb()))


def comment_order_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(comment, Order_KB.filter(action='comment'), state=None)
    dp.register_callback_query_handler(stop_comment, Cat_KB.filter(action='stop_comment'), state='*')
    dp.register_message_handler(write_comment, state=CommentToOrder.write_comment)
