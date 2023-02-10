from aiogram import Dispatcher
from keyboards.client_kb import *
from aiogram import types
from aiogram.utils import exceptions
from user_handlers.handler import edit_text


async def price_cat(query: types.CallbackQuery):
    await edit_text(message=query.message, message_text='Category:', reply_markup=cat_markup())


async def price_brand(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні бренди в категорії:',
                    reply_markup=brand_markup(callback_data['id']))


async def price_position(query: types.CallbackQuery, callback_data: dict):
    await edit_text(query.message, message_text='Доступні смаки бренду:',
                    reply_markup=position_markup(callback_data['id'], price=True))


async def price_single_position(query: types.CallbackQuery, callback_data: dict):
    await query.message.delete()
    text = sqlite_db.select_one_position(callback_data['id'])
    full_text = f'{text[0]} {text[1]} {text[2]} {text[3]} {text[4]}'
    try:
        await query.bot.send_photo(chat_id=query.message.chat.id,
                                   photo=types.InputFile(
                                       fr"image/{callback_data['id']}.png"),
                                   caption=f'{full_text}\n',
                                   reply_markup=back_to.back_to_order_menu())
    except FileNotFoundError:

        await query.bot.send_message(text=f'{full_text}\n'
                                          f'Кількість: 0, Ціна: {text[5]}'
                                     , reply_markup=back_to.back_to_menu(), chat_id=query.message.chat.id)


def register_price_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(price_cat, Menu_KB.filter(action='price'))
    dp.register_callback_query_handler(price_brand, Cat_KB.filter(action='from_cat_to_brand'))
    dp.register_callback_query_handler(price_position, Cat_KB.filter(action='from_brand_to_pos'))
    dp.register_callback_query_handler(price_single_position, Cat_KB.filter(action='price_single_position'))
