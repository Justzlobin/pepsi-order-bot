from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from classes import Order

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
                    reply_markup=order_menu_kb().add(back_to_menu_kb()))


async def new_custom(query: types.CallbackQuery):
    order.start_order(query.from_user.id)
    text = f'{order.order_dict}'
    await edit_text(query.message, message_text=text, reply_markup=order_kb().add(back_to_menu_kb()))


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
    full_text = 'Ваше замовлення\n'
    print(order.order_dict)
    for pos, value in order.order_dict[query.from_user.id].items():
        dict_desc = sqlite_db.select_one_position(pos)
        full_text.join(
            f"{dict_desc['brand_title']} {dict_desc['tasty_title']} {dict_desc['size']} --"
            f" {dict_desc['price'] * value}\n")

    await edit_text(message=query.message, message_text=full_text,
                    reply_markup=order_kb())


async def order_settings(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Налаштування замовлення:',
                    reply_markup=keyboard_settings(
                        sqlite_db.select_last_order(query.from_user.id)))


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
    print(order.order_dict)
    print(order.pos_dict)


async def cmd_numbers(query: types.CallbackQuery, callback_data: dict):
    if str(callback_data['id']) in order.order_dict[query.from_user.id].keys():
        value = order.order_dict[query.from_user.id][callback_data['id']]
        order.pos_dict[query.from_user.id][callback_data['id']] = value
    else:
        order.add_in_pos_dict(query.from_user.id, callback_data['id'], 0)
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
                                                        f'Кількість: {value}, Ціна: {dict_desc["price"] * value} uah.',
                    reply_markup=keyboard(callback_data['id']).add(back_to(back_to_pos=callback_data['id'])))


async def order_position_plus(query: types.CallbackQuery, callback_data: dict):
    user_value = order.pos_dict[query.from_user.id][callback_data['id']]
    result = user_value + sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[order.checkin]
    order.pos_dict[query.from_user.id][callback_data['id']] = result
    await update_num_text(query.message,
                          result,
                          callback_data['id'])


async def order_position_minus(query: types.CallbackQuery, callback_data: dict):
    user_value = order.pos_dict[query.from_user.id][callback_data['id']]
    result = user_value - sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[order.checkin]
    if result < 0:
        result = 0
    order.pos_dict[query.from_user.id][callback_data['id']] = result
    await update_num_text(query.message,
                          result,
                          callback_data['id'])


async def order_position_zero(query: types.CallbackQuery, callback_data: dict):
    order.pos_dict[query.from_user.id][callback_data['id']] = 0
    await update_num_text(query.message, 0, callback_data['id'])


async def order_position_finish(query: types.CallbackQuery, callback_data: dict):
    print(order.order_dict)
    print(order.pos_dict)
    dict_desc = sqlite_db.select_one_position(callback_data['id'])
    full_text = f"{dict_desc['brand_title']} {dict_desc['size']} {dict_desc['type']} " \
                f"{dict_desc['tasty_title']} {dict_desc['tasty_desc']}\n" \
        # f"Ціна: {dict_desc['price']} грн.\n" \
    # f"В ящику: {dict_desc['box_size']} ящ.\n" \
    # f"Ціна за ящик: {dict_desc['price'] * dict_desc['box_size']} грн."
    quantity = order.pos_dict[query.from_user.id][callback_data['id']]
    amount = round(dict_desc['price'] * quantity, 2)

    if quantity != 0:
        await query.answer(f'Добавлено: {full_text}\n'
                           f'К-ть: {quantity}, Ціна: {amount}')
        order.add_in_order_dict(query.from_user.id, callback_data['id'], quantity)
    if quantity == 0:
        del order.pos_dict[query.from_user.id][callback_data['id']]
        del order.order_dict[query.from_user.id][callback_data['id']]

    await edit_text(query.message, message_text='Доступні смаки бренду:',
                    reply_markup=position_markup(sqlite_db.select_brand_id(callback_data['id'])).add(
                        back_to(back_to_brand_from_pos=callback_data['id'])
                    ))
    print(order.order_dict)
    print(order.pos_dict)


async def box(query: types.CallbackQuery):
    order.checkin = True
    await query.answer(text='Обрано в ящиках')


async def multi(query: types.CallbackQuery):
    order.checkin = False
    await query.answer(text='Обрано поштучно')


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

    dp.register_callback_query_handler(order_position_finish, Cat_KB.filter(action='finish'))
    #
    dp.register_callback_query_handler(box, Cat_KB.filter(action='box'))
    dp.register_callback_query_handler(multi, Cat_KB.filter(action='multi'))
