from aiogram import Dispatcher
from keyboards import *
from aiogram import types
from user_handlers.handler import edit_text, order, status, delete_message
from text.text_in_message import main_menu, menu_order, menu
from aiogram.utils import exceptions


async def back_to_cat_from_brand(query: types.CallbackQuery):
    try:
        if status.dialog_status[query.from_user.id] == 'price':
            await edit_text(message=query.message, message_text='Категорії:',
                            reply_markup=cat_markup().add(back_to_menu_kb()))
        if status.dialog_status[query.from_user.id] == 'order':
            await edit_text(message=query.message, message_text='Категорії:',
                            reply_markup=cat_markup().add(back_to_order_kb()))
    except KeyError:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())


async def back_to_brand_from_tasty(query: types.CallbackQuery, callback_data: dict):
    try:
        if status.dialog_status[query.from_user.id] == 'price':
            await edit_text(query.message, message_text='Бренди:',
                            reply_markup=brand_markup(callback_data['id']).add(
                                back_to_cat_from_brand_kb(), back_to_menu_kb()))
        if status.dialog_status[query.from_user.id] == 'order':
            await edit_text(query.message, message_text='Бренди:',
                            reply_markup=brand_markup(callback_data['id']).add(
                                back_to_cat_from_brand_kb(), back_to_order_kb()))
    except KeyError:
        await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())


async def back_to_tasty_from_pos(query: types.CallbackQuery, callback_data: dict):
    await query.message.delete()

    brand_id = sqlite_db.select_brand_id(callback_data['id'])
    print(f'{callback_data["id"]} - pos_id?')
    print(f'brand_id {type(brand_id)}  - {brand_id}')
    try:
        if status.dialog_status[query.from_user.id] == 'price':
            message = await query.bot.send_message(chat_id=query.message.chat.id, text='Смаки:',
                                                   reply_markup=position_markup(brand_id,
                                                                                status.dialog_status[
                                                                                    query.from_user.id]).row(
                                                       back_to_brand_from_tasty_kb(
                                                           sqlite_db.select_cat_id(brand_id)),
                                                       back_to_menu_kb()))
            delete_message.change_message(user_id=query.from_user.id, message_id=message)

        if status.dialog_status[query.from_user.id] == 'order':
            message = await query.bot.send_message(chat_id=query.message.chat.id, text='Смаки:',
                                                   reply_markup=position_markup(brand_id,
                                                                                status.dialog_status[
                                                                                    query.from_user.id]).row(
                                                       back_to_brand_from_tasty_kb(
                                                           sqlite_db.select_cat_id(brand_id)),
                                                       back_to_order_kb()))
            delete_message.change_message(user_id=query.from_user.id, message_id=message)

        if status.dialog_status[query.from_user.id] == 'admin':
            message = await query.bot.send_message(chat_id=query.message.chat.id, text='Смаки:',
                                                   reply_markup=position_markup(brand_id,
                                                                                status.dialog_status[
                                                                                    query.from_user.id]).row(
                                                       back_to_brand_from_tasty_kb(
                                                           sqlite_db.select_cat_id(brand_id)),
                                                       back_to_admin_menu_kb()))
            delete_message.change_message(user_id=query.from_user.id, message_id=message)

    except KeyError:
        message = await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())
        delete_message.change_message(user_id=query.from_user.id, message_id=message)
    except exceptions.MessageToEditNotFound:
        message = await edit_text(message=query.message, message_text=main_menu, reply_markup=menu_kb())
        delete_message.change_message(user_id=query.from_user.id, message_id=message)



async def back_to_main_menu(query: types.CallbackQuery):
    await edit_text(query.message, reply_markup=menu_kb(),
                    message_text='<b>PEPSIBOT</b>\n'
                                 f'{main_menu}')


async def back_to_order_menu(query: types.CallbackQuery):
    try:
        if order.order_dict[query.from_user.id]:
            await edit_text(message=query.message,
                            message_text='‼ В корзині залишились продукти ‼\n'
                                         '<b>Вийти і видалити</b> чи <b>Продовжити замовлення ❔</b>',
                            reply_markup=chose_next_move_in_order_kb())
        else:
            await edit_text(query.message,
                            message_text=menu,
                            reply_markup=order_menu_kb().add(back_to_menu_kb()))
    except KeyError:
        await edit_text(query.message,
                        message_text=menu,
                        reply_markup=order_menu_kb().add(back_to_menu_kb()))


async def back_to_start_order(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text=menu_order,
                    reply_markup=order_kb().add(back_to_order_menu_kb()))


async def back_to_order_settings(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text='⚙ Налаштування замовлення:',
                    reply_markup=keyboard_settings().add(back_to_order_kb()))


def register_back_to_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_tasty_from_pos, Back_to_id.filter(action='back_to_tasty_from_pos'))
    dp.register_callback_query_handler(back_to_cat_from_brand, Back_to.filter(action='back_to_cat_from_brand'))
    dp.register_callback_query_handler(back_to_brand_from_tasty, Back_to_id.filter(action='back_to_brand_from_tasty'))
    dp.register_callback_query_handler(back_to_order_menu, Back_to.filter(action='back_to_order_menu'))
    dp.register_callback_query_handler(back_to_start_order, Back_to.filter(action='back_to_start_order'))
    dp.register_callback_query_handler(back_to_main_menu, Back_to.filter(action='back_to_menu'))
    dp.register_callback_query_handler(back_to_order_settings, Back_to.filter(action='back_to_order_settings'))
