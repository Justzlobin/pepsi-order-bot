from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


