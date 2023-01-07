from aiogram.utils import executor


from create_bot import dp
from handlers import *
from datadase import sqlite_db


async def on_startup(_):
    print("Бот вийшов онлайн")
    sqlite_db.start_db()

register_handler.register_register_handlers(dp)
handler.register_handlers_handler(dp)


comment.comment_order_handlers(dp)
update_order_handler.register_update_order_handler(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
