from aiogram import Dispatcher
from keyboards.client_kb import *
from keyboards.back_to import *
from aiogram import types
from user_handlers.handler import edit_text, status, photo


async def price_cat(query: types.CallbackQuery):
    status.current_dialog_status_price(query.from_user.id)
    await edit_text(message=query.message, message_text='Category:', reply_markup=cat_markup().add(back_to_menu_kb()))


async def price_brand(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні бренди в категорії:',
                    reply_markup=brand_markup(callback_data['id']).add(
                        back_to_cat_from_brand_kb()))


async def price_tasty(query: types.CallbackQuery, callback_data: dict):
    print(callback_data['id'])
    print('price_tasty id')
    brand_id = callback_data['id']
    await edit_text(query.message, message_text='price_handler:',
                    reply_markup=position_markup(brand_id, status.dialog_status[query.from_user.id]).add(
                        back_to_brand_from_tasty_kb(sqlite_db.select_cat_id(brand_id))))


async def price_show_position(query: types.CallbackQuery, callback_data: dict):
    dict_desc = sqlite_db.select_one_position(callback_data['id'])
    full_text = f"{dict_desc['brand_title']} {dict_desc['size']} {dict_desc['type']} " \
                f"{dict_desc['tasty_title']} {dict_desc['tasty_desc']}\n" \
                f"Ціна: {dict_desc['price']} грн.\n" \
                f"В ящику: {dict_desc['box_size']} ящ.\n" \
                f"Ціна за ящик: {dict_desc['price'] * dict_desc['box_size']} грн."
    try:
        message_photo = await query.bot.send_photo(chat_id=query.message.chat.id,
                                                   photo=types.InputFile(
                                                       fr"image/{callback_data['id']}.png"),
                                                   reply_markup=keyboard(callback_data['id']))
        photo.add(chat_id=query.message.chat.id, photo=message_photo)
    except FileNotFoundError:
        pass
    brand_id = sqlite_db.select_brand_id(callback_data['id'])
    await edit_text(message=query.message, message_text=full_text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=back_to_tasty_from_pos_kb(brand_id)))


def register_price_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(price_cat, Menu_KB.filter(action='price'))
    dp.register_callback_query_handler(price_brand, Cat_KB.filter(action='from_cat_to_brand'))
    dp.register_callback_query_handler(price_tasty, Cat_KB.filter(action='from_brand_to_tasty'))
    dp.register_callback_query_handler(price_show_position, Cat_KB.filter(action='price_show_position'))
