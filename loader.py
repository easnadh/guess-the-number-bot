from aiogram import Bot, Dispatcher

from config import load_config

config = load_config()

bot: Bot = Bot(token=config.tg_bot.token.get_secret_value(), parse_mode='HTML')

dp: Dispatcher = Dispatcher()
