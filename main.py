import asyncio
import logging

import handlers
from db.base import session_maker, async_engine, Base
from db.engine import get_models
from loader import dp, bot
from middlewares.register_check import RegisterCheck


async def main():
    logging.basicConfig(level=logging.DEBUG)

    print('Bot started')
    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())
    dp.include_router(handlers.router)

    await get_models(async_engine, Base.metadata)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
