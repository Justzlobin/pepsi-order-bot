from aiogram import Dispatcher
from create_bot import dp
from keyboards import *


async def calendar(query: types.CallbackQuery):
    await dp.bot.send_message(text='select date', chat_id=query.message.chat.id,
                              reply_markup=start_calendar())


async def payment(query: types.CallbackQuery):
    await dp.bot.send_message(text='Оберіть спосіб оплати:',
                              chat_id=query.message.chat.id,
                              reply_markup=chose_payment(query.from_user.id))
    await query.message.delete()


async def payment_cash(query: types.CallbackQuery):
    await query.bot.send_message(text='Обрано: "💰 Готівка"', reply_markup=order_menu_kb(),
                                 chat_id=query.message.chat.id)
    sqlite_db.update_payment(query.from_user.id, payment='💰 Готівка')
    await query.message.delete()


async def payment_bank(query: types.CallbackQuery):
    await query.bot.send_message(text='Обрано: "💳 Банк"', reply_markup=order_menu_kb(),
                                 chat_id=query.message.chat.id)
    sqlite_db.update_payment(query.from_user.id, payment='💳 Банк')
    await query.message.delete()


def register_order_settings(dp: Dispatcher):
    dp.register_callback_query_handler(calendar, cat_cb.filter(action='date_deliver'))
    dp.register_callback_query_handler(payment, cat_cb.filter(action='payment'))
    dp.register_callback_query_handler(payment_cash, cat_cb.filter(action='cash'))
    dp.register_callback_query_handler(payment_bank, cat_cb.filter(action='bank'))
