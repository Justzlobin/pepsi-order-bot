from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from user_handlers.handler import edit_text


async def back_to_cat(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Оберіть цікаву вам категорію:',
                    reply_markup=cat_markup())


async def back_to_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні смаки бренду:',
                    reply_markup=position_markup(callback_data['id']))


async def back_to_menu_from_order(query: types.CallbackQuery):
    await edit_text(query.message, reply_markup=menu_kb(),
                    message_text='<b>PEPSIBOT</b>\n'
                                 'Натисніть:\n'
                                 '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
                                 'або сформувати замовлення. \n'
                                 '<b>🗃 Історія замовлень</b> - переглянути попередні замовлення.\n'
                                 '<b>📝 Реєстрація</b> - щоб розуміти кому відправляти замовлення.\n')


async def back_to_order_menu(query: types.CallbackQuery):
    await edit_text(query.message,
                    message_text='1. Натисність <b>🛍️ Товари</b>, щоб почати формувати замовлення.\n'
                                 '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
                                 '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
                    reply_markup=order_kb().add(back_to_menu_kb()))


def register_back_to_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_menu_from_order, Back_to.filter(action='back_to_menu'))
    dp.register_callback_query_handler(back_to_cat, Cat_KB.filter(action='back_to_cat'))
    dp.register_callback_query_handler(back_to_position, Cat_KB.filter(action='back_to_position'))
    dp.register_callback_query_handler(back_to_order_menu, Back_to.filter(action='back_to_order_menu'))
