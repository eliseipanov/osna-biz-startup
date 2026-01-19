import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from bot.handlers.start import router as start_router
from bot.handlers.store import router as store_router
from bot.handlers.order import router as order_router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(store_router)
dp.include_router(order_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())