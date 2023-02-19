from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from classes import Order

user_data = {}
order_data = {}
checkin = False

order = Order()


async def command_start(message: types.Message):
    await message.delete()
    await message.bot.send_message(message.from_user.id,
                                   text='<b>PEPSIBOT</b>\n'
                                        'MAIN MENU',
                                   reply_markup=menu_kb().add(back_to_menu_kb()),
                                   parse_mode='HTML')


async def order_menu(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text='ORDER_MENU',
                    reply_markup=order_menu_kb())


async def new_custom(query: types.CallbackQuery):
    order.start_order(query.from_user.id)
    text = f'{order.order_dict}'
    await edit_text(query.message, message_text=text, reply_markup=order_kb())


async def last_order(query: types.CallbackQuery):
    sqlite_db.delete_empty_orders()
    sqlite_db.delete_not_verification(user_id=query.from_user.id)
    await edit_text(query.message, message_text='Останні замовлення:',
                    reply_markup=order_for_user(query.from_user.id).add(back_to_order_menu_kb()))


async def order_product_list(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Оберіть цікаву вам категорію:',
                    reply_markup=cat_markup().add(back_to_order_kb()))


async def show_brand(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні бренди в категорії:',
                    reply_markup=brand_markup(callback_data['id']).add(back_to(back_to_cat_from_brand=True)))


async def show_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні смаки бренду:',
                    reply_markup=position_markup(callback_data['id']).add(
                        back_to(back_to_brand_from_pos=callback_data['id'])))


async def order_basket(query: types.CallbackQuery):
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
    await edit_text(message=query.message, message_text=order.order_dict,
                    reply_markup=order_kb())


async def order_settings(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Налаштування замовлення:',
                    reply_markup=keyboard_settings(
                        sqlite_db.select_last_order(query.from_user.id)))


async def order_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text=f'{sqlite_db.select_one_position(callback_data["id"])}\n'
                                                f'Кількість: 0, Ціна: {callback_data["id"][4]}',
                    reply_markup=keyboard(callback_data['id']))


async def update_num_text(message: types.Message, new_value: int, pos_id):
    dict_desc = sqlite_db.select_one_position(pos_id)
    full_text = f"{dict_desc['brand_title']} {dict_desc['size']} {dict_desc['type']} " \
                f"{dict_desc['tasty_title']} {dict_desc['tasty_desc']}\n" \
                f"Ціна: {dict_desc['price']} грн.\n" \
                f"В ящику: {dict_desc['box_size']} ящ.\n" \
                f"Ціна за ящик: {dict_desc['price'] * dict_desc['box_size']} грн."
    await message.edit_text(text=f'{full_text}\n'
                                 f'К-ть: {new_value}, Ціна: {round(float(dict_desc["price"]) * new_value, 2)}, '
                                 f'Уп: {sqlite_db.select_price_of_box(pos_id, new_value)} '
                            , reply_markup=keyboard(pos_id).add(back_to(back_to_pos=pos_id)))


async def cmd_numbers(query: types.CallbackQuery, callback_data: dict):
    print(order.order_dict[query.from_user.id].items())
    if callback_data['id'] in order.order_dict[query.from_user.id].items():
        value = order.order_dict[query.from_user.id][callback_data['id']]
    else:
        order.add_pos(query.from_user.id, callback_data['id'], 0)
        value = 0
    dict_desc = sqlite_db.select_one_position(callback_data['id'])
    full_text = f"{dict_desc['brand_title']} {dict_desc['size']} {dict_desc['type']} " \
                f"{dict_desc['tasty_title']} {dict_desc['tasty_desc']}\n" \
                f"Ціна: {dict_desc['price']} грн.\n" \
                f"В ящику: {dict_desc['box_size']} ящ.\n" \
                f"Ціна за ящик: {dict_desc['price'] * dict_desc['box_size']} грн."
    # try:
    #     message_photo = await query.bot.send_photo(chat_id=query.message.chat.id,
    #                                                photo=types.InputFile(
    #                                                    fr"image/{callback_data['id']}.png"),
    #                                                caption=f'{full_text}\n'
    #                                                        f'Кількість: 0, Ціна: {text[5]}',
    #                                                reply_markup=keyboard(callback_data['id']))
    # except FileNotFoundError:

    await edit_text(message=query.message, message_text=f'{full_text}\n'
                                                        f'Кількість: {value}, Ціна: {dict_desc["price"]} uah.',
                    reply_markup=keyboard(callback_data['id']).add(back_to(back_to_pos=callback_data['id'])))


async def order_position_plus(query: types.CallbackQuery, callback_data: dict):
    user_value = order.order_dict[query.from_user.id][callback_data['id']]
    result = user_value + sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[checkin]
    order.order_dict[query.from_user.id][callback_data['id']] = result
    await update_num_text(query.message,
                          result,
                          callback_data['id'])


async def order_position_minus(query: types.CallbackQuery, callback_data: dict):
    user_value = order.order_dict[query.from_user.id][callback_data['id']]
    result = user_value - sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[checkin]
    if result < 0:
        result = 0
    order.order_dict[query.from_user.id][callback_data['id']] = result
    await update_num_text(query.message,
                          result,
                          callback_data['id'])


async def order_position_zero(query: types.CallbackQuery, callback_data: dict):
    order.order_dict[query.from_user.id][callback_data['id']] = 0
    await update_num_text(query.message, 0, callback_data['id'])


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
    await edit_text(query.message, message_text='Доступні смаки бренду:',
                    reply_markup=position_markup(sqlite_db.select_brand_id(callback_data['id'])))


async def box(query: types.CallbackQuery):
    global checkin
    checkin = True
    await query.answer(text='Обрано в ящиках')


async def multi(query: types.CallbackQuery):
    global checkin
    checkin = False
    await query.answer(text='Обрано поштучно')


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


async def edit_text(message: types.Message, message_text, reply_markup):
    await message.edit_text(text=message_text, reply_markup=reply_markup, parse_mode='HTML')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    # MAIN_MENU
    dp.register_callback_query_handler(order_menu, Menu_KB.filter(action='order_menu'))
    # MAIN_ORDER
    dp.register_callback_query_handler(new_custom, Order_KB.filter(action='new_order'))
    dp.register_callback_query_handler(last_order, Order_KB.filter(action='last_order'))
    # MENU_NEW_ORDER
    dp.register_callback_query_handler(order_product_list, Order_KB.filter(action='order_product_list'))
    dp.register_callback_query_handler(order_basket, Order_KB.filter(action='order_basket'))
    dp.register_callback_query_handler(order_settings, Order_KB.filter(action='order_settings'))
    #
    dp.register_callback_query_handler(show_brand, Cat_KB.filter(action='cat->brand'))
    dp.register_callback_query_handler(show_position, Cat_KB.filter(action='brand->pos'))
    dp.register_callback_query_handler(cmd_numbers, Cat_KB.filter(action='position'))
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
