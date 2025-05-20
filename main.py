import asyncio

import logging

from core.init_bot import bot, dp
from handlers.user_handlers import user_router
from database.init_db import init_database


async def main():
    logging.basicConfig(level=logging.INFO)
    
    await init_database()
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        pass