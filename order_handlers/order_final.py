# from aiogram import Dispatcher
# from keyboards import *
# from user_handlers.handler import order_data
# from user_handlers.handler import edit_text
#
#
# async def delete_from_order(query: types.CallbackQuery):
#     sqlite_db.delete_from_order(order_data[f'{query.from_user.id}'])
#     await edit_text(query.message, message_text='*Замовлення скасовано!*\n'
#                                                 '<b>PEPSIBOT</b>\n'
#                                                 'Натисніть:\n'
#                                                 '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
#                                                 'або сформувати замовлення. \n'
#                                                 '<b>🗃 Історія замовлень</b> - переглянути попередні замовлення.\n'
#                                                 '<b>📝 Реєстрація</b> - щоб розуміти кому відправляти замовлення.',
#                     reply_markup=menu_kb())
#
#
# async def add_in_list_orders(query: types.CallbackQuery, callback_data: dict):
#     await query.answer(text='Замовлення збережено!')
#     sqlite_db.order_verification(callback_data['id'])
#     await edit_text(query.message, message_text='*Ще одне замовлення?*\n'
#                                                 '<b>PEPSIBOT</b>\n'
#                                                 'Натисніть:\n'
#                                                 '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
#                                                 'або сформувати замовлення. \n'
#                                                 '<b>🗃 Історія замовлень</b> - переглянути попередні замовлення.\n'
#                                                 '<b>📝 Реєстрація</b> - щоб розуміти кому відправляти замовлення.',
#                     reply_markup=menu_kb())
#
#
# async def order_continue(query: types.CallbackQuery):
#     await edit_text(query.message, message_text='1. Натисність <b>🛍️ Товари</b>, щоб почати формувати замовлення.\n'
#                                                 '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
#                                                 '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
#                     reply_markup=order_menu_kb())
#
#
# def register_order_final(dp: Dispatcher):
#     dp.register_callback_query_handler(add_in_list_orders, Cat_KB.filter(action='add_full_order'))
#     dp.register_callback_query_handler(delete_from_order, Cat_KB.filter(action='delete_from_order'))
#     dp.register_callback_query_handler(order_continue, Cat_KB.filter(action='continue_to_order'))
