import asyncio
import logging
from src import config
from src.handlers import support_handlers, user_handlers, admin_handlers
from aiogram import Bot, Dispatcher

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

if config.LOGGING:
    logging.basicConfig(format='[+] %(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


dp.include_routers(admin_handlers.rt, support_handlers.rt, user_handlers.rt)


async def main():
    b = Bot(token=config.BOT_TOKEN)
    await dp.start_polling(b, skip_updates=True)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
