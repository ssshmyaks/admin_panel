import asyncio
import logging
import config
import admin_handlers
import user_handlers
import distribute
from aiogram import Bot, Dispatcher

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

if config.LOGGING:
    logging.basicConfig(format='[+] %(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


dp.include_routers(admin_handlers.rt, user_handlers.rt, distribute.rt)


async def main():
    b = Bot(token=config.BOT_TOKEN)
    await dp.start_polling(b, skip_updates=True)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
