from aiogram import Dispatcher
from keyboards import *
from user_handlers.handler import edit_text, order


async def calendar(query: types.CallbackQuery):
    await edit_text(query.message, message_text='select date',
                    reply_markup=start_calendar())


async def payment(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Оберіть спосіб оплати:',
                    reply_markup=chose_payment(query.from_user.id))


async def payment_cash(query: types.CallbackQuery):
    await edit_text(query.message, message_text='*Обрано: "💰 Готівка"*\n'
                                                '1. Натисність <b>🛍️ Товари</b>, щоб почати формувати замовлення.\n'
                                                '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
                                                '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
                    reply_markup=order_menu_kb())
    order.order_settings_dict(user_id=query.from_user.id, payment='💰 Готівка')


async def payment_bank(query: types.CallbackQuery):
    await edit_text(query.message, message_text='*Обрано: "💳 Банк"*\n'
                                                '1. Натисність <b>🛍️ Товари</b>, щоб почати формувати замовлення.\n'
                                                '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
                                                '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
                    reply_markup=order_menu_kb())
    order.order_settings_dict(user_id=query.from_user.id, payment='💳 Банк')


def register_order_settings(dp: Dispatcher):
    dp.register_callback_query_handler(calendar, Cat_KB.filter(action='date_deliver'))
    dp.register_callback_query_handler(payment, Cat_KB.filter(action='payment'))
    dp.register_callback_query_handler(payment_cash, Cat_KB.filter(action='cash'))
    dp.register_callback_query_handler(payment_bank, Cat_KB.filter(action='bank'))
