from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from classes import Order, Status
from classes.delete import DeleteMessage
from text.text_in_message import main_menu, menu_order, menu
from aiogram.utils import exceptions

order = Order()
status = Status()
delete_message = DeleteMessage()


async def command_start(message: types.Message):
    await message.delete()
    try:
        await delete_message.delete_message_dict[message.chat.id].delete()
    except KeyError:
        pass
    except exceptions.MessageToDeleteNotFound:
        pass
    message = await message.bot.send_message(message.from_user.id, text='<b>PEPSIBOT</b>\n'
                                                                        f'{main_menu}',
                                             reply_markup=menu_kb(), parse_mode='HTML')
    delete_message.change_message(user_id=message.chat.id, message_id=message)
    print(f'message_dict = {delete_message.delete_message_dict}')
    print(f'message = {message}')
    print(f'user_id = {message.chat.id}')
    print(f'user_name = {message.from_user.first_name} {message.from_user.last_name}')


async def order_menu(query: types.CallbackQuery):
    if sqlite_db.user_exist(query.from_user.id):
        await edit_text(message=query.message, message_text=menu,
                        reply_markup=order_menu_kb().add(register_kb(button=True), back_to_menu_kb()))
    else:
        await edit_text(message=query.message, message_text=menu,
                        reply_markup=register_kb().add(back_to_menu_kb()))


async def new_custom(query: types.CallbackQuery):
    status.current_dialog_status_order(query.from_user.id)
    order.start_order(query.from_user.id)
    await edit_text(query.message, message_text=menu_order, reply_markup=order_kb().add(back_to_order_menu_kb()))


async def last_order(query: types.CallbackQuery):
    await edit_text(query.message, message_text='🕐 Останні замовлення:',
                    reply_markup=order_for_user(query.from_user.id).add(back_to_order_menu_kb()))


async def order_product_list(query: types.CallbackQuery):
    await edit_text(query.message, message_text='Категорії:',
                    reply_markup=cat_markup().add(back_to_order_kb()))


async def order_basket(query: types.CallbackQuery):
    try:
        if order.order_dict[query.from_user.id]:
            date_deliver_order = order.date_deliver[query.from_user.id].strftime("%d/%m/%Y")
            payment = order.order_settings_dict[query.from_user.id]['payment']
            comment = order.order_settings_dict[query.from_user.id]['comment']
            full_text = 'Ваше замовлення.\n' \
                        f'Дата доставки: {date_deliver_order}\n' \
                        f'Спосіб оплати: {payment}\n' \
                        f'Примітки: {comment}\n'
            total = 0
            print(order.order_dict)
            for key, value in order.order_dict[query.from_user.id].items():
                dict_desc = sqlite_db.select_one_position(int(key))
                full_text += ' '.join(
                    [f"{dict_desc['brand_title']} {dict_desc['tasty_title']} {dict_desc['size']} --"
                     f" {round(dict_desc['price'] * value, 2)}\n"])
                total += round(dict_desc["price"] * value, 2)

            full_text += f'Сума замовлення: {total}'
            await edit_text(message=query.message, message_text=full_text,
                            reply_markup=order_basket_kb().add(back_to_order_kb()))
        else:
            await query.answer(text='Корзина пуста')
            await edit_text(message=query.message, message_text=menu_order,
                            reply_markup=order_kb().add(back_to_order_menu_kb()))
    except KeyError:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())


async def order_settings(query: types.CallbackQuery):
    await edit_text(query.message, message_text='⚙ Налаштування замовлення:',
                    reply_markup=keyboard_settings().add(back_to_order_kb()))


async def update_num_text(message: types.Message, new_value: int, pos_id):
    try:
        await message.edit_caption(caption=update_message(pos_id=pos_id, value=new_value),
                                   reply_markup=keyboard(
                                       pos_id, box=order.checkin[message.chat.id]).add(
                                       back_to_tasty_from_pos_kb(pos_id)))
    except exceptions.BadRequest:
        await message.edit_text(text=update_message(pos_id=pos_id, value=new_value),
                                reply_markup=keyboard(
                                    pos_id, box=order.checkin[message.chat.id]).add(
                                    back_to_tasty_from_pos_kb(pos_id)))
    print(order.order_dict)
    print(order.pos_dict)


async def position(query: types.CallbackQuery, callback_data: dict):
    value = 0
    try:
        if str(callback_data['id']) in order.order_dict[query.from_user.id].keys():
            value = order.order_dict[query.from_user.id][callback_data['id']]
            order.pos_dict[query.from_user.id][callback_data['id']] = value
        else:
            order.add_in_pos_dict(query.from_user.id, callback_data['id'], 0)
    except KeyError:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())

    try:
        message = await query.bot.send_photo(chat_id=query.message.chat.id,
                                             photo=types.InputFile(
                                                 fr"image/{callback_data['id']}.png"),
                                             caption=update_message(callback_data['id'], value=value),
                                             reply_markup=keyboard(callback_data['id'],
                                                                   box=order.checkin[
                                                                       query.from_user.id]).add(
                                                 back_to_tasty_from_pos_kb(callback_data['id'])))
    except FileNotFoundError:
        message = await query.bot.send_message(chat_id=query.message.chat.id,
                                               text=update_message(callback_data['id'], value=value),
                                               reply_markup=keyboard(callback_data['id'],
                                                                     box=order.checkin[
                                                                         query.from_user.id]).add(
                                                   back_to_tasty_from_pos_kb(callback_data['id'])))
    delete_message.change_message(user_id=query.from_user.id, message_id=message)
    await query.message.delete()

    print(f'pos_id {callback_data["id"]}')


async def order_position_plus(query: types.CallbackQuery, callback_data: dict):
    user_value = order.pos_dict[query.from_user.id][callback_data['id']]
    result = user_value + sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[
        order.checkin[query.from_user.id]]
    order.pos_dict[query.from_user.id][callback_data['id']] = result
    await update_num_text(query.message,
                          result,
                          callback_data['id'])


async def order_position_minus(query: types.CallbackQuery, callback_data: dict):
    user_value = order.pos_dict[query.from_user.id][callback_data['id']]
    result = user_value - sqlite_db.select_multiplicity_and_box_size(callback_data['id'])[
        order.checkin[query.from_user.id]]
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
    await query.message.delete()

    dict_desc = sqlite_db.select_one_position(callback_data['id'])
    full_text = f"{dict_desc['brand_title']} {dict_desc['size']} {dict_desc['type']} " \
                f"{dict_desc['tasty_title']} {dict_desc['tasty_desc']}\n"
    quantity = order.pos_dict[query.from_user.id][callback_data['id']]
    amount = round(dict_desc['price'] * quantity, 2)

    if quantity != 0:
        await query.answer(f'Добавлено: {full_text}\n'
                           f'К-ть: {quantity}, Ціна: {amount}')
        order.add_in_order_dict(query.from_user.id, callback_data['id'], quantity)
    if quantity == 0:
        try:
            del order.pos_dict[query.from_user.id][callback_data['id']]
        except KeyError:
            pass
        try:
            del order.order_dict[query.from_user.id][callback_data['id']]
        except KeyError:
            pass
    brand_id = sqlite_db.select_brand_id(callback_data['id'])
    await query.bot.send_message(text='Доступні смаки бренду:',
                                 reply_markup=position_markup(brand_id, status.dialog_status[query.from_user.id]).add(
                                     back_to_brand_from_tasty_kb(sqlite_db.select_cat_id(brand_id))),
                                 chat_id=query.message.chat.id)


async def box(query: types.CallbackQuery):
    order.checkin[query.from_user.id] = True
    await query.answer(text='Обрано в ящиках')


async def multi(query: types.CallbackQuery, callback_data: dict):
    def multi_bool():
        if order.checkin[query.from_user.id] is True:
            return False
        else:
            return True

    order.checkin[query.from_user.id] = multi_bool()
    order.pos_dict[query.from_user.id][callback_data['id']] = 0
    try:
        await update_num_text(query.message, 0, callback_data['id'])
    except exceptions.BadRequest:
        pass

    print(order.checkin[query.from_user.id])


async def edit_text(message: types.Message, message_text, reply_markup):
    await message.edit_text(text=message_text, reply_markup=reply_markup, parse_mode='HTML')


async def messages(message):
    await message.delete()



def update_message(pos_id, value) -> str:
    dict_desc = sqlite_db.select_one_position(pos_id)
    full_text = f"{dict_desc['brand_title']} {dict_desc['size']} {dict_desc['type']} " \
                f"{dict_desc['tasty_title']} {dict_desc['tasty_desc']}\n" \
                f"Ціна: {dict_desc['price']} грн.\n" \
                f"В ящику: {dict_desc['box_size']} ящ.\n" \
                f"Ціна за ящик: {round(dict_desc['price'] * dict_desc['box_size'], 2)} грн.\n" \
                f"__________________________________\n" \
                f"К-ть: {value}, Ціна: {round(value * dict_desc['price'], 2)}," \
                f" к-ть уп: {round(value / dict_desc['box_size'], 1)}"
    return full_text


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
    dp.register_callback_query_handler(position, Cat_KB.filter(action='position'))
    #
    dp.register_callback_query_handler(order_position_plus, Cat_KB.filter(action='incr'))
    dp.register_callback_query_handler(order_position_minus, Cat_KB.filter(action='desc'))
    dp.register_callback_query_handler(order_position_zero, Cat_KB.filter(action='zero'))
    dp.register_callback_query_handler(order_position_finish, Cat_KB.filter(action='finish'))
    #
    dp.register_callback_query_handler(box, Cat_KB.filter(action='box'))
    dp.register_callback_query_handler(multi, Cat_KB.filter(action='multi'))
    # #
    # dp.register_message_handler(messages, content_types=types.ContentType.STICKER)
    # dp.register_message_handler(messages, content_types=types.ContentType.ANIMATION)
    # dp.register_message_handler(messages, content_types=types.ContentType.AUDIO)
    # dp.register_message_handler(messages, content_types=types.ContentType.VIDEO)
    # dp.register_message_handler(messages, content_types=types.ContentType.VOICE)
    # dp.register_message_handler(messages, content_types=types.ContentType.PHOTO)
    # dp.register_message_handler(messages, content_types=types.ContentType.DOCUMENT)
    # dp.register_message_handler(messages, content_types=types.ContentType.LOCATION)
    dp.register_message_handler(messages, content_types=types.ContentType.ANY)
    # dp.register_message_handler(messages)
