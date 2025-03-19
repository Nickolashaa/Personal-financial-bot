from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
import asyncio
from bot.handlers import router
from aiogram.client.default import DefaultBotProperties


async def main():
    bot = Bot(token=os.getenv("TG_TOKEN"), default=DefaultBotProperties(parse_mode="HTML"))
    print("Бот инициализирован")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        dp = Dispatcher()
        dp.include_router(router)
        load_dotenv()
        asyncio.run(main())
    except KeyboardInterrupt:
        pass