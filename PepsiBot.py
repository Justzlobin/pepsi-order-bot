from aiogram.utils import executor
from admin_handlers import *
from order_handlers import *
from create_bot import dp
from user_handlers import *
from datadase import sqlite_db


async def on_startup(_):
    print("Бот вийшов онлайн")
    sqlite_db.start_db()


register_handler.register_register_handlers(dp)
handler.register_user_handlers(dp)
admin_check_order.register_admin_handlers(dp)
comment.comment_order_handlers(dp)
update_order_handler.register_update_order_handler(dp)
order_settings.register_order_settings(dp)
order_final.register_order_final(dp)
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
