import aiogram.utils.exceptions
from aiogram import Dispatcher
from create_bot import dp
from keyboards import *
from config import ADMIN

user_data = {}
order_data = {}
checkin = False


async def command_start(message: types.Message):
    await message.bot.send_message(message.from_user.id, 'Ласкаво просимо в <b>PepsiBot</b>!\n'
                                                         'Бот створений для прийому заявок,\n'
                                                         'а також як інтерактивний прайс з продукцією.\n'
                                                         'Якщо ви вперше тут,\n'
                                                         'прошу натиснути 📋 <b>Реєстрація</b>\n'
                                                         'щоб <b>PepsiBot</b> розумів,\n'
                                                         'кому і куди відправляти замовлення!',

                                   reply_markup=menu_kb(), parse_mode='HTML')
    await message.delete()


async def back_to_main_menu(query: types.CallbackQuery):
    await query.bot.send_message(query.from_user.id, 'Ласкаво просимо в <b>PepsiBot</b>!\n'
                                                     'Бот створений для прийому заявок,\n'
                                                     'а також як інтерактивний прайс з продукцією.\n'
                                                     'Якщо ви вперше тут,\n'
                                                     'прошу натиснути 📋 <b>Реєстрація</b>\n'
                                                     'щоб <b>PepsiBot</b> розумів,\n'
                                                     'кому і куди відправляти замовлення!',

                                 reply_markup=menu_kb(), parse_mode='HTML')
    await query.message.delete()


async def command_assort(query: types.CallbackQuery):
    await query.message.delete()
    try:
        await query.bot.send_message(query.from_user.id, 'Оберіть цікаву вам категорію:', reply_markup=order_menu_kb())
    except KeyError:
        await query.bot.send_message(query.from_user.id, 'Нажаль, час сесії вийшов\n'
                                                         'Оберіть цікаву вам категорію:', reply_markup=order_menu_kb())


async def back_to_cat(query: types.CallbackQuery):
    await dp.bot.send_message(text='Оберіть цікаву вам категорію:', chat_id=query.message.chat.id,
                              reply_markup=cat_markup())
    await query.message.delete()


async def show_brand(query: types.CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    await dp.bot.send_message(text='Доступні бренди в категорії:', chat_id=chat_id,
                              reply_markup=brand_markup(callback_data['id']))
    await query.message.delete()


async def show_position(query: types.CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    await dp.bot.send_message(text='Доступні смаки бренду:', chat_id=chat_id,
                              reply_markup=position_markup(callback_data['id']))

    await query.message.delete()


async def back_to_position(query: types.CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    await dp.bot.send_message(text='Доступні смаки бренду:', chat_id=chat_id,
                              reply_markup=position_markup(callback_data['id']))
    await query.message.delete()


async def order_position(query: types.CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id

    await dp.bot.send_message(text=f'{sqlite_db.select_one_position(callback_data["id"])}\n'
                                   f'Кількість: 0, Ціна: {callback_data["id"][4]}', chat_id=chat_id,
                              reply_markup=keyboard(callback_data['id']))

    await query.message.delete()


async def update_num_text(message: types.Message, new_value: int, pos_id):
    text = sqlite_db.select_one_position(pos_id)
    full_text = f'{text[0]} {text[1]} {text[2]} {text[3]} {text[4]}'
    await message.edit_text(text=f'{full_text}\n'
                                 f'К-ть: {new_value}, Ціна: {round(float(text[5]) * new_value, 2)}, '
                                 f'Уп: {sqlite_db.select_price_of_box(pos_id, new_value)} '
                            , reply_markup=keyboard(pos_id))


async def cmd_numbers(query: types.CallbackQuery, callback_data: dict):
    user_data[callback_data['id']] = 0

    text = sqlite_db.select_one_position(callback_data['id'])
    full_text = f'{text[0]} {text[1]} {text[2]} {text[3]} {text[4]}'
    await query.message.answer(text=f'{full_text}\n'
                                    f'Кількість: 0, Ціна: {text[5]}'
                               , reply_markup=keyboard(callback_data['id']))
    await query.message.delete()
    print(user_data)


async def order_position_plus(query: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(callback_data['id'])
    print('user_value:' + str(user_value))
    result = user_value + sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[checkin]
    user_data[callback_data['id']] = result
    print('user_data ' + str(result))
    print(user_data)
    await update_num_text(query.message,
                          result,
                          callback_data['id'])


async def order_position_minus(query: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(callback_data['id'], 0)
    result = user_value - sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[checkin]

    if result < 0:
        result = 0
    user_data[callback_data['id']] = result
    await update_num_text(query.message,
                          result,
                          callback_data['id'])


async def order_position_zero(query: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(callback_data['id'], 0)
    user_data[callback_data['id']] = user_value - user_value

    await update_num_text(query.message, user_value - user_value, callback_data['id'])


async def order_position_finish(query: types.CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    text = sqlite_db.select_one_position(callback_data['id'])
    full_text = f'{text[0]} {text[1]} {text[2]} {text[3]} {text[4]}'
    quantity = user_data[callback_data['id']]
    sum = quantity * text[5]
    try:
        if quantity != 0:
            await query.answer(f'Добавлено: {full_text}\n'
                               f'К-ть: {quantity}, Ціна: {round(sum, 2)}')
            sqlite_db.add_in_order(order_data[f'{query.from_user.id}'],
                                   callback_data['id'],
                                   quantity,
                                   round(sum, 2),
                                   query.from_user.id)

        else:
            pass
    except KeyError:
        await query.bot.send_message(query.from_user.id, 'Нажаль, час сесії вийшов\n'
                                                         'Головне меню:', reply_markup=menu_kb())

    await query.message.delete()
    await dp.bot.send_message(text='Доступні смаки бренду', chat_id=chat_id,
                              reply_markup=position_markup(sqlite_db.select_brand_id(callback_data['id'])))


async def order_view(message: types.Message):
    try:
        if sqlite_db.sum_order(order_data[f'{message.from_user.id}']) == 0:
            await message.answer(text='Корзина пуста')
        else:
            await message.answer(
                text=f'Ваше замовлення: <b>{sqlite_db.sum_order(order_data[f"{message.from_user.id}"])}</b>',
                reply_markup=keyboard_order(order_data[f'{message.from_user.id}'],
                                            message.from_user.id),
                parse_mode='HTML')
    except KeyError:
        await message.bot.send_message(message.from_user.id, 'Нажаль, час сесії вийшов\n'
                                       , reply_markup=menu_kb())


async def add_in_list_orders(query: types.CallbackQuery, callback_data: dict):
    await query.answer(text='Замовлення збережено!')
    sqlite_db.order_verification(callback_data['id'])
    await query.message.delete()
    await query.bot.send_message(text='Ще одне замовлення?)', chat_id=query.message.chat.id, reply_markup=menu_kb())


async def new_custom(query: types.CallbackQuery):
    await query.bot.send_message(text='1. Натисність <b>🛍️ Асортимент</b>, щоб почати формувати замовлення.\n'
                                      '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
                                      '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
                                 reply_markup=order_menu_kb(), parse_mode='HTML', chat_id=query.message.chat.id)
    new_custom = sqlite_db.create_new_custom(query.from_user.id)
    order_data[f'{query.from_user.id}'] = new_custom
    await query.message.delete()
    print(order_data)
    print(f'new custom: {new_custom}')


async def delete_from_order(query: types.CallbackQuery):
    sqlite_db.delete_from_order(order_data[f'{query.from_user.id}'])
    await query.answer(text='Замовлення скасовано!')
    await query.message.delete()


async def box(query: types.CallbackQuery):
    global checkin
    checkin = True
    await query.answer(text='Обрано в ящиках')


async def multi(query: types.CallbackQuery):
    global checkin
    checkin = False
    await query.answer(text='Обрано поштучно')


async def last_order(query: types.CallbackQuery):
    sqlite_db.delete_empty_orders()
    sqlite_db.delete_not_verification(user_id=query.from_user.id)
    await query.bot.send_message(text='Останні замовлення:',
                                 reply_markup=order_for_user(query.from_user.id),
                                 chat_id=query.message.chat.id)


async def update_numbers(query: types.CallbackQuery, callback_data: dict):
    sum1 = user_data[callback_data['id']]

    update_text = sqlite_db.select_one_position(callback_data['id'])
    full_text = f'{update_text[0]} {update_text[1]} {update_text[2]} {update_text[3]} {update_text[4]}'
    order = True
    await query.message.answer(text=f'{full_text}\n'
                                    f'Кількість: {sum1}, Ціна: {update_text[5]}'
                               , reply_markup=keyboard(callback_data['id'], order))
    await query.message.delete()


async def update_order_finish(query: types.CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id

    sqlite_db.update_order_pos_id(user_data[callback_data['id']],
                                  sqlite_db.select_last_order(query.from_user.id),
                                  callback_data['id'])

    await dp.bot.send_message(
        text=f'Ваше замовлення: <b>{sqlite_db.sum_order(order_data[f"{query.from_user.id}"])}</b>',
        chat_id=chat_id,
        reply_markup=keyboard_order(sqlite_db.select_last_order(query.from_user.id),
                                    query.from_user.id), parse_mode='HTML')
    await query.message.delete()


async def update_plus(query: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(callback_data['id'])
    result = user_value + sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[checkin]
    user_data[callback_data['id']] = result
    await update_num_text_in_order(query.message, result, callback_data['id'])


async def update_zero(query: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(callback_data['id'], 0)
    user_data[callback_data['id']] = user_value - user_value
    await update_num_text_in_order(query.message, user_value - user_value, callback_data['id'])


async def update_minus(query: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(callback_data['id'], 0)
    result = user_value - sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[checkin]

    if result < 0:
        result = 0
    user_data[callback_data['id']] = result
    await update_num_text_in_order(query.message, result, callback_data['id'])


async def update_num_text_in_order(message: types.Message, new_value: int, pos_id):
    text = sqlite_db.select_one_position(pos_id)
    full_text = f'{text[0]} {text[1]} {text[2]} {text[3]} {text[4]}'

    await message.edit_text(text=f'{full_text}\n'
                                 f'Кількість: {new_value}, Ціна: {round(float(text[5]) * new_value, 2)}',
                            reply_markup=keyboard(pos_id, order=True))


async def order_settings(message: types.Message):
    user_id = message.from_user.id
    await message.delete()
    await message.answer(text='Налаштування замовлення:',
                         reply_markup=keyboard_settings(sqlite_db.select_last_order(user_id)))


async def calendar(query: types.CallbackQuery):
    await dp.bot.send_message(text='select date', chat_id=query.message.chat.id,
                              reply_markup=start_calendar())


async def payment(query: types.CallbackQuery):
    await dp.bot.send_message(text='Оберіть спосіб оплати:',
                              chat_id=query.message.chat.id,
                              reply_markup=chose_payment(query.from_user.id))
    await query.message.delete()


async def payment_cash(query: types.CallbackQuery):
    await query.answer(text='Обрано: "💰 Готівка"')
    sqlite_db.update_payment(query.from_user.id, payment='💰 Готівка')
    await query.message.delete()


async def payment_bank(query: types.CallbackQuery):
    await query.answer(text='Обрано: "💳 Банк"')
    sqlite_db.update_payment(query.from_user.id, payment='💳 Банк')
    await query.message.delete()


async def back_to_menu_from_order(message: types.Message):
    user_data[f'{message.from_user.id}'] = None
    await message.delete()
    await message.answer(reply_markup=menu_kb(), text='Ви повернулись в меню!')


async def order_continue(query: types.CallbackQuery):
    await query.message.delete()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    #
    dp.register_callback_query_handler(back_to_menu_from_order, Menu_KB.filter(action='back_to_menu'))
    dp.register_callback_query_handler(command_assort, order_kb.filter(action='assort'))
    dp.register_callback_query_handler(order_view, order_kb.filter(action='basket'))
    dp.register_callback_query_handler(order_settings, order_kb.filter(action='settings'))
    #
    dp.register_callback_query_handler(new_custom, Menu_KB.filter(action='new_order'))
    dp.register_callback_query_handler(last_order, Menu_KB.filter(action='last_orders'))
    dp.register_message_handler(back_to_menu_from_order, text='🔙 Назад до меню')
    #
    dp.register_callback_query_handler(show_brand, cat_cb.filter(action='cat->brand'))
    dp.register_callback_query_handler(show_position, cat_cb.filter(action='brand->pos'))
    dp.register_callback_query_handler(cmd_numbers, cat_cb.filter(action='position'))
    #
    dp.register_callback_query_handler(back_to_cat, cat_cb.filter(action='back_to_cat'))
    dp.register_callback_query_handler(back_to_position, cat_cb.filter(action='back_to_position'))
    #
    dp.register_callback_query_handler(order_position_plus, cat_cb.filter(action='incr'))
    dp.register_callback_query_handler(order_position_minus, cat_cb.filter(action='desc'))
    dp.register_callback_query_handler(order_position_zero, cat_cb.filter(action='zero'))
    dp.register_callback_query_handler(update_order_finish, cat_cb.filter(action='update_finish'))
    dp.register_callback_query_handler(order_position_finish, cat_cb.filter(action='finish'))

    dp.register_callback_query_handler(box, cat_cb.filter(action='box'))
    dp.register_callback_query_handler(multi, cat_cb.filter(action='multi'))
    #
    dp.register_callback_query_handler(add_in_list_orders, cat_cb.filter(action='add_full_order'))
    dp.register_callback_query_handler(delete_from_order, cat_cb.filter(action='delete_from_order'))
    dp.register_callback_query_handler(order_continue, cat_cb.filter(action='continue_from_order'))
    #
    dp.register_callback_query_handler(update_numbers, cat_cb.filter(action='position_order'))

    #
    dp.register_callback_query_handler(update_plus, cat_cb.filter(action='update_incr'))
    dp.register_callback_query_handler(update_minus, cat_cb.filter(action='update_desc'))
    dp.register_callback_query_handler(update_zero, cat_cb.filter(action='update_zero'))

    dp.register_callback_query_handler(calendar, cat_cb.filter(action='date_deliver'))
    dp.register_callback_query_handler(payment, cat_cb.filter(action='payment'))
    dp.register_callback_query_handler(payment_cash, cat_cb.filter(action='cash'))
    dp.register_callback_query_handler(payment_bank, cat_cb.filter(action='bank'))