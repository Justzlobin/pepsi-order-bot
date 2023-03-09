from aiogram import Dispatcher
from keyboards import *
from keyboards.calendar_kb import SimpleCalendar, calendar_callback as simple_cal_callback
from user_handlers.handler import edit_text, order
from text.text_in_message import menu_order
from classes.select_date import SelectDate

date_dict = SelectDate()


async def date_deliver_message(query: types.CallbackQuery):
    await edit_text(query.message, message_text='select date history',
                    reply_markup=date_deliver_kb(date_from=date_dict.select_date['from'],
                                                 date_to=date_dict.select_date['to']))


async def calendar(query: types.CallbackQuery):
    await edit_text(query.message, message_text='select date',
                    reply_markup=await SimpleCalendar().start_calendar())


async def payment(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Оберіть спосіб оплати:',
                    reply_markup=chose_payment())


async def payment_cash(query: types.CallbackQuery):
    await query.answer(text='Cash!')
    await edit_text(query.message, message_text=menu_order,
                    reply_markup=order_kb().add(back_to_menu_kb()))
    order.order_settings_dict(user_id=query.from_user.id, payment='💰 Готівка')


async def payment_bank(query: types.CallbackQuery):
    await query.answer(text='Bank!')
    await edit_text(query.message, message_text=menu_order,
                    reply_markup=order_kb().add(back_to_menu_kb()))
    order.order_settings_dict(user_id=query.from_user.id, payment='💳 Банк')


async def process_simple_calendar(query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(query, callback_data)
    if selected:
        date_dict.select_date_from(query.from_user.id, date.strftime("%d/%m/%Y"))
        await query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
            reply_markup=keyboard_settings()
        )


def register_order_settings(dp: Dispatcher):
    dp.register_callback_query_handler(date_deliver_message, Order_KB.filter(action='date_deliver'))
    dp.register_callback_query_handler(calendar, Order_KB.filter(action='date_deliver_from'))
    dp.register_callback_query_handler(payment, Order_KB.filter(action='payment'))
    dp.register_callback_query_handler(payment_cash, Order_KB.filter(action='cash'))
    dp.register_callback_query_handler(payment_bank, Order_KB.filter(action='bank'))
    dp.register_callback_query_handler(process_simple_calendar, simple_cal_callback.filter())
