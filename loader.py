from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_config

config = load_config()
storage = MemoryStorage()

bot: Bot = Bot(token=config.tg_bot.token.get_secret_value(), parse_mode='HTML')

dp: Dispatcher = Dispatcher(storage=storage)
