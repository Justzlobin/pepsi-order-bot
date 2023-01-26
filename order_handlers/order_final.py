from aiogram import Dispatcher
from keyboards import *
from user_handlers.handler import order_data
from user_handlers.handler import del_mes, delete_message_from_dict


async def delete_from_order(query: types.CallbackQuery):
    sqlite_db.delete_from_order(order_data[f'{query.from_user.id}'])
    message = await query.bot.send_message(text='*Замовлення скасовано!*'
                                                '<b>PEPSIBOT</b>\n'
                                                'Натисніть:\n'
                                                '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
                                                '                       або сформувати замовлення. \n'
                                                '<b>🗃 Історія замовлень</b> - переглянути попередні\n'
                                                '                              замовлення.\n'
                                                '<b>📝 Реєстрація</b> - щоб розуміти кому\n'
                                                '                       відправляти замовлення.\n',
                                           reply_markup=menu_kb(),
                                           chat_id=query.message.chat.id)
    del_mes.add_message(chat_id=query.message.chat.id, message_id=message)
    await delete_message_from_dict(chat=query.message.chat.id)


async def add_in_list_orders(query: types.CallbackQuery, callback_data: dict):
    await query.answer(text='Замовлення збережено!')
    sqlite_db.order_verification(callback_data['id'])
    message = await query.bot.send_message(text='*Ще одне замовлення?*'
                                                '<b>PEPSIBOT</b>\n'
                                                'Натисніть:\n'
                                                '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
                                                '                       або сформувати замовлення. \n'
                                                '<b>🗃 Історія замовлень</b> - переглянути попередні\n'
                                                '                              замовлення.\n'
                                                '<b>📝 Реєстрація</b> - щоб розуміти кому\n'
                                                '                       відправляти замовлення.\n',
                                           chat_id=query.message.chat.id,
                                           reply_markup=menu_kb())
    del_mes.add_message(chat_id=query.message.chat.id, message_id=message)
    await delete_message_from_dict(chat=query.message.chat.id)


async def order_continue(query: types.CallbackQuery):
    message = await query.bot.send_message(text='1. Натисність <b>🛍️ Товари</b>, щоб почати формувати замовлення.\n'
                                                '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
                                                '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
                                           chat_id=query.message.chat.id,
                                           reply_markup=order_menu_kb())
    del_mes.add_message(chat_id=query.message.chat.id, message_id=message)
    await delete_message_from_dict(chat=query.message.chat.id)


def register_order_final(dp: Dispatcher):
    dp.register_callback_query_handler(add_in_list_orders, Cat_KB.filter(action='add_full_order'))
    dp.register_callback_query_handler(delete_from_order, Cat_KB.filter(action='delete_from_order'))
    dp.register_callback_query_handler(order_continue, Cat_KB.filter(action='continue_to_order'))
