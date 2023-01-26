from aiogram import Dispatcher
from create_bot import dp
from keyboards import *
from user_handlers.handler import del_mes, delete_message_from_dict


async def calendar(query: types.CallbackQuery):
    await dp.bot.send_message(text='select date', chat_id=query.message.chat.id,
                              reply_markup=start_calendar())


async def payment(query: types.CallbackQuery):
    message = await dp.bot.send_message(text='Оберіть спосіб оплати:',
                                        chat_id=query.message.chat.id,
                                        reply_markup=chose_payment(query.from_user.id))
    del_mes.add_message(chat_id=query.message.chat.id, message_id=message)
    await delete_message_from_dict(chat=query.message.chat.id)


async def payment_cash(query: types.CallbackQuery):
    message = await query.bot.send_message(text='*Обрано: "💰 Готівка"*\n'
                                                '1. Натисність <b>🛍️ Товари</b>, щоб почати формувати замовлення.\n'
                                                '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
                                                '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
                                           reply_markup=order_menu_kb(),
                                           chat_id=query.message.chat.id)
    sqlite_db.update_payment(query.from_user.id, payment='💰 Готівка')
    del_mes.add_message(chat_id=query.message.chat.id, message_id=message)
    await delete_message_from_dict(chat=query.message.chat.id)


async def payment_bank(query: types.CallbackQuery):
    message = await query.bot.send_message(text='*Обрано: "💳 Банк"*\n'
                                                '1. Натисність <b>🛍️ Товари</b>, щоб почати формувати замовлення.\n'
                                                '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
                                                '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
                                           reply_markup=order_menu_kb(),
                                           chat_id=query.message.chat.id)
    sqlite_db.update_payment(query.from_user.id, payment='💳 Банк')
    del_mes.add_message(chat_id=query.message.chat.id, message_id=message)
    await delete_message_from_dict(chat=query.message.chat.id)


def register_order_settings(dp: Dispatcher):
    dp.register_callback_query_handler(calendar, Cat_KB.filter(action='date_deliver'))
    dp.register_callback_query_handler(payment, Cat_KB.filter(action='payment'))
    dp.register_callback_query_handler(payment_cash, Cat_KB.filter(action='cash'))
    dp.register_callback_query_handler(payment_bank, Cat_KB.filter(action='bank'))
