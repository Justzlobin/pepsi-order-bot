from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from classes import Order
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

user_data = {}
order_data = {}
checkin = False

order = Order()


async def command_start(message: types.Message):
    await message.delete()
    await message.bot.send_message(message.from_user.id,
                                   text='<b>PEPSIBOT</b>\n'
                                        'Натисніть:\n'
                                        '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
                                        'або сформувати замовлення. \n'
                                        '<b>🗃 Історія замовлень</b> - переглянути попередні замовлення.\n'
                                        '<b>📝 Реєстрація</b> - щоб розуміти кому відправляти замовлення.\n',

                                   reply_markup=InlineKeyboardMarkup.add(order_menu_kb(), menu_kb()),
                                   parse_mode='HTML')


async def command_assort(query: types.CallbackQuery):
    try:
        await edit_text(query.message, message_text='Оберіть цікаву вам категорію:',
                        reply_markup=cat_markup())
    except KeyError:
        await edit_text(query.message, message_text='Оберіть цікаву вам категорію:',
                        reply_markup=cat_markup())


async def back_to_cat(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Оберіть цікаву вам категорію:',
                    reply_markup=cat_markup())


async def show_brand(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні бренди в категорії:',
                    reply_markup=brand_markup(callback_data['id']))


async def show_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні смаки бренду:',
                    reply_markup=position_markup(callback_data['id']))


async def back_to_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні смаки бренду:',
                    reply_markup=position_markup(callback_data['id']))
    # try:
    #     await delete_message_from_dict(chat=query.message.chat.id)
    # except exceptions.MessageToDeleteNotFound:
    #     pass


async def order_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text=f'{sqlite_db.select_one_position(callback_data["id"])}\n'
                                                f'Кількість: 0, Ціна: {callback_data["id"][4]}',
                    reply_markup=keyboard(callback_data['id']))


async def update_num_text(message: types.Message, new_value: int, pos_id):
    text = sqlite_db.select_one_position(pos_id)
    full_text = f'{text[0]} {text[1]} {text[2]} {text[3]} {text[4]}'
    await message.edit_text(text=f'{full_text}\n'
                                 f'К-ть: {new_value}, Ціна: {round(float(text[5]) * new_value, 2)}, '
                                 f'Уп: {sqlite_db.select_price_of_box(pos_id, new_value)} '
                            , reply_markup=keyboard(pos_id))


async def cmd_numbers(query: types.CallbackQuery, callback_data: dict):
    await query.message.delete()
    user_data[callback_data['id']] = 0
    text = sqlite_db.select_one_position(callback_data['id'])
    full_text = f'{text[0]} {text[1]} {text[2]} {text[3]} {text[4]}'
    try:
        message_photo = await query.bot.send_photo(chat_id=query.message.chat.id,
                                                   photo=types.InputFile(
                                                       fr"image/{callback_data['id']}.png"),
                                                   caption=f'{full_text}\n'
                                                           f'Кількість: 0, Ціна: {text[5]}',
                                                   reply_markup=keyboard(callback_data['id']))
    except FileNotFoundError:

        await query.bot.send_message(text=f'{full_text}\n'
                                          f'Кількість: 0, Ціна: {text[5]}'
                                     , reply_markup=keyboard(callback_data['id']), chat_id=query.message.chat.id)


async def order_position_plus(query: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(callback_data['id'])
    result = user_value + sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[checkin]
    user_data[callback_data['id']] = result
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
        await query.answer(text='Час для замовлення вийшов.')
        await edit_text(query.message,
                        message_text='<b>PEPSIBOT</b>\n'
                                     'Натисніть:\n'
                                     '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
                                     'або сформувати замовлення. \n'
                                     '<b>🗃 Історія замовлень</b> - переглянути попередні замовлення.\n'
                                     '<b>📝 Реєстрація</b> - щоб розуміти кому відправляти замовлення.\n',
                        reply_markup=menu_kb())
    # try:
    #     await delete_message_from_dict(chat=query.message.chat.id)
    # except exceptions.MessageToDeleteNotFound:
    #     pass
    await edit_text(query.message, message_text='Доступні смаки бренду:',
                    reply_markup=position_markup(sqlite_db.select_brand_id(callback_data['id'])))


async def order_view(query: types.CallbackQuery):
    # try:
    #     if sqlite_db.sum_order(order_data[f'{query.from_user.id}']) == 0:
    #         await query.answer(text='Корзина пуста')
    #     else:
    #         await edit_text(query.message,
    #                         message_text=
    #                         f'Ваше замовлення: <b>{sqlite_db.sum_order(order_data[f"{query.from_user.id}"])}</b>',
    #                         reply_markup=keyboard_order(order_data[f'{query.from_user.id}'], query.from_user.id))
    # except KeyError:
    #     await query.answer(text='Час для замовлення вийшов.')
    #     await edit_text(query.message,
    #                     message_text='<b>PEPSIBOT</b>\n'
    #                                  'Натисніть:\n'
    #                                  '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
    #                                  'або сформувати замовлення. \n'
    #                                  '<b>🗃 Історія замовлень</b> - переглянути попередні замовлення.\n'
    #                                  '<b>📝 Реєстрація</b> - щоб розуміти кому відправляти замовлення.\n'
    #                     , reply_markup=menu_kb())
    order.add_pos(query.from_user.id, 3, 4)
    await query.bot.send_message(text=order.order_dict, chat_id=query.message.chat.id,
                                 reply_markup=InlineKeyboardMarkup.add(menu_kb(), order_menu_kb()))


async def new_custom(query: types.CallbackQuery):
    text = """New order...."""
    # new_custom = sqlite_db.create_new_custom(query.from_user.id)
    # order_data[f'{query.from_user.id}'] = new_custom
    order.start_order(query.from_user.id)
    await edit_text(query.message, message_text=text, reply_markup=order_menu_kb())


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
    await edit_text(query.message, message_text='Останні замовлення:',
                    reply_markup=order_for_user(query.from_user.id))


async def update_numbers(query: types.CallbackQuery, callback_data: dict):
    sum1 = user_data[callback_data['id']]
    update_text = sqlite_db.select_one_position(callback_data['id'])
    full_text = f'{update_text[0]} {update_text[1]} {update_text[2]} {update_text[3]} {update_text[4]}'
    order = True
    await edit_text(query.message, message_text=f'{full_text}\n'
                                                f'Кількість: {sum1}, Ціна: {update_text[5]}'
                    , reply_markup=keyboard(callback_data['id'], order))


async def update_order_finish(query: types.CallbackQuery, callback_data: dict):
    sqlite_db.update_order_pos_id(user_data[callback_data['id']],
                                  sqlite_db.select_last_order(query.from_user.id),
                                  callback_data['id'])
    await edit_text(query.message,
                    message_text=f'Ваше замовлення: <b>{sqlite_db.sum_order(order_data[f"{query.from_user.id}"])}</b>',
                    reply_markup=keyboard_order(sqlite_db.select_last_order(query.from_user.id),
                                                query.from_user.id))
    # try:
    #     await delete_message_from_dict(chat=query.message.chat.id)
    # except exceptions.MessageToDeleteNotFound:
    #     pass


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

    await edit_text(message, message_text=f'{full_text}\n'
                                          f'Кількість: {new_value}, Ціна: {round(float(text[5]) * new_value, 2)}',
                    reply_markup=keyboard(pos_id, order=True))


async def order_settings(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Налаштування замовлення:',
                    reply_markup=keyboard_settings(
                        sqlite_db.select_last_order(query.from_user.id)))


async def back_to_menu_from_order(query: types.CallbackQuery):
    await edit_text(query.message, reply_markup=menu_kb(),
                    message_text='<b>PEPSIBOT</b>\n'
                                 'Натисніть:\n'
                                 '<b>💲 Замовлення</b> - щоб переглянути асортимент\n'
                                 'або сформувати замовлення. \n'
                                 '<b>🗃 Історія замовлень</b> - переглянути попередні замовлення.\n'
                                 '<b>📝 Реєстрація</b> - щоб розуміти кому відправляти замовлення.\n')
    user_data[f'{query.from_user.id}'] = None


async def back_to_order_menu(query: types.CallbackQuery):
    await edit_text(query.message,
                    message_text='1. Натисність <b>🛍️ Товари</b>, щоб почати формувати замовлення.\n'
                                 '2. <b>🛒 Корзина</b>, щоб перевірити та підтвердити заамовлення.\n'
                                 '3. <b>⚙ Налаштування</b>, щоб внести свої побажання чи дату доставки.',
                    reply_markup=order_menu_kb())


async def edit_text(message: types.Message, message_text, reply_markup):
    await message.edit_text(text=message_text, reply_markup=reply_markup, parse_mode='HTML')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    #
    dp.register_callback_query_handler(back_to_menu_from_order, Back_to.filter(action='back_to_menu'))
    dp.register_callback_query_handler(command_assort, Order_KB.filter(action='assort'))
    dp.register_callback_query_handler(order_view, Order_KB.filter(action='basket'))
    dp.register_callback_query_handler(order_settings, Order_KB.filter(action='settings'))
    #
    dp.register_callback_query_handler(new_custom, Menu_KB.filter(action='new_order'))
    dp.register_callback_query_handler(last_order, Menu_KB.filter(action='last_orders'))
    #
    dp.register_callback_query_handler(show_brand, Cat_KB.filter(action='cat->brand'))
    dp.register_callback_query_handler(show_position, Cat_KB.filter(action='brand->pos'))
    dp.register_callback_query_handler(cmd_numbers, Cat_KB.filter(action='position'))
    #
    dp.register_callback_query_handler(back_to_cat, Cat_KB.filter(action='back_to_cat'))
    dp.register_callback_query_handler(back_to_position, Cat_KB.filter(action='back_to_position'))
    dp.register_callback_query_handler(back_to_order_menu, Back_to.filter(action='back_to_order_menu'))
    #
    dp.register_callback_query_handler(order_position_plus, Cat_KB.filter(action='incr'))
    dp.register_callback_query_handler(order_position_minus, Cat_KB.filter(action='desc'))
    dp.register_callback_query_handler(order_position_zero, Cat_KB.filter(action='zero'))
    dp.register_callback_query_handler(update_order_finish, Cat_KB.filter(action='update_finish'))
    dp.register_callback_query_handler(order_position_finish, Cat_KB.filter(action='finish'))
    #
    dp.register_callback_query_handler(box, Cat_KB.filter(action='box'))
    dp.register_callback_query_handler(multi, Cat_KB.filter(action='multi'))
    #
    dp.register_callback_query_handler(update_numbers, Cat_KB.filter(action='position_order'))
    dp.register_callback_query_handler(update_plus, Cat_KB.filter(action='update_incr'))
    dp.register_callback_query_handler(update_minus, Cat_KB.filter(action='update_desc'))
    dp.register_callback_query_handler(update_zero, Cat_KB.filter(action='update_zero'))
