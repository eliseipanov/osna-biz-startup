import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from bot.handlers.start import register_start_handlers

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

register_start_handlers(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())