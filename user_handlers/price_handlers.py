from aiogram import Dispatcher

from keyboards.client_kb import *
from aiogram import types
from user_handlers.handler import edit_text


async def price_cat(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text='Category:', reply_markup=cat_markup(price=True))


async def price_brand(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні бренди в категорії:',
                    reply_markup=brand_markup(callback_data['id'], price=True))


async def price_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні смаки бренду:',
                    reply_markup=position_markup(callback_data['id'], price=True))


async def price_single_position(query: types.CallbackQuery, callback_data: dict):
    await query.message.delete()
    dict_desc = sqlite_db.select_one_position(callback_data['id'])
    full_text = f"{dict_desc['brand_title']} {dict_desc['size']} {dict_desc['type']} " \
                f"{dict_desc['tasty_title']} {dict_desc['tasty_desc']}\n" \
                f"Ціна: {dict_desc['price']} грн.\n" \
                f"В ящику: {dict_desc['box_size']} ящ.\n" \
                f"Ціна за ящик: {dict_desc['price'] * dict_desc['box_size']} грн."
    try:
        await query.bot.send_photo(chat_id=query.message.chat.id,
                                   photo=types.InputFile(
                                       fr"image/{callback_data['id']}.png"),
                                   caption=f'{full_text}\n',
                                   reply_markup=back_to_position_kb(callback_data['id'], price=True))
    except FileNotFoundError:
        await edit_text(message=query.message, message_text=f'{full_text}\n'
                        , reply_markup=back_to_position_kb(callback_data['id'], price=True), )


async def price_back_to_cat_from_brand(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text='Category:', reply_markup=cat_markup(price=True))


async def price_back_to_brand_from_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(message=query.message, message_text='Brands:',
                    reply_markup=brand_markup(cat_id=callback_data['id'], price=True))


async def price_back_to_position(query: types.CallbackQuery, callback_data: dict):
    await query.message.delete()
    await query.bot.send_message(text='tasties of brand',
                                 reply_markup=position_markup(
                                     brand_id=callback_data['id'],
                                     price=True),
                                 chat_id=query.message.chat.id)


def register_price_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(price_cat, Menu_KB.filter(action='price'))
    dp.register_callback_query_handler(price_brand, Cat_KB.filter(action='from_cat_to_brand'))
    dp.register_callback_query_handler(price_position, Cat_KB.filter(action='from_brand_to_pos'))
    dp.register_callback_query_handler(price_single_position, Cat_KB.filter(action='price_single_position'))
    dp.register_callback_query_handler(price_back_to_cat_from_brand, Cat_KB.filter(action='price_back_to_cat'))
    dp.register_callback_query_handler(price_back_to_brand_from_position, Cat_KB.filter(action='price_back_to_brand'))
    dp.register_callback_query_handler(price_back_to_position, Cat_KB.filter(action='price_back_to_position'))
