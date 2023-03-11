from aiogram import Dispatcher
from keyboards import *
from keyboards.calendar_kb import SimpleCalendar, calendar_callback as simple_cal_callback
from user_handlers.handler import edit_text, order
from text.text_in_message import menu_order, main_menu
import datetime


async def date_deliver_message(query: types.CallbackQuery):
    try:
        date = order.date_deliver[query.from_user.id].strftime("%d/%m/%Y")
        await edit_text(query.message, message_text='Дата доставки:',
                        reply_markup=date_deliver_kb(date=date).add(back_to_order_settings_kb()))
    except KeyError:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())


async def calendar(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Оберіть зручну для вас дату:',
                    reply_markup=(await SimpleCalendar().start_calendar()).add(back_to_order_settings_kb()))


async def payment(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Оберіть спосіб оплати:',
                    reply_markup=chose_payment().add(back_to_order_settings_kb()))


async def payment_cash(query: types.CallbackQuery):
    await query.answer(text='Cash!')
    await edit_text(query.message, message_text=menu_order,
                    reply_markup=keyboard_settings().add(back_to_order_kb()))
    order.order_settings_dict(user_id=query.from_user.id, payment='💰 Готівка')


async def payment_bank(query: types.CallbackQuery):
    await query.answer(text='Bank!')
    await edit_text(query.message, message_text=menu_order,
                    reply_markup=keyboard_settings().add(back_to_order_kb()))
    order.order_settings_dict(user_id=query.from_user.id, payment='💳 Банк')


async def process_simple_calendar(query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(query, callback_data)
    print(date)
    print(datetime.datetime.today())
    try:
        if selected:
            if date <= datetime.datetime.today():
                await edit_text(message=query.message, message_text='‼ Некоректна дата ‼',
                                reply_markup=date_deliver_kb(
                                    date=order.date_deliver[query.from_user.id].strftime("%d/%m/%Y")).add(
                                    back_to_order_settings_kb()))
            else:
                order.change_date_deliver(query.from_user.id, date)
                await edit_text(message=query.message, message_text=f'You selected {date.strftime("%d/%m/%Y")}',
                                reply_markup=date_deliver_kb(
                                    date=order.date_deliver[query.from_user.id].strftime("%d/%m/%Y")).add(
                                    back_to_order_settings_kb()))
    except KeyError:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())


def register_order_settings(dp: Dispatcher):
    dp.register_callback_query_handler(date_deliver_message, Order_KB.filter(action='date_deliver'))
    dp.register_callback_query_handler(calendar, Order_KB.filter(action='date_deliver_change'))
    dp.register_callback_query_handler(payment, Order_KB.filter(action='payment'))
    dp.register_callback_query_handler(payment_cash, Order_KB.filter(action='cash'))
    dp.register_callback_query_handler(payment_bank, Order_KB.filter(action='bank'))
    dp.register_callback_query_handler(process_simple_calendar, simple_cal_callback.filter())
