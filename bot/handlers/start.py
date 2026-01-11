from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from core.database import async_session
from core.models import User

async def start_handler(message: Message):
    tg_id = message.from_user.id
    full_name = message.from_user.full_name

    async with async_session() as session:
        user = await session.get(User, tg_id)
        if user:
            user.full_name = full_name
        else:
            user = User(tg_id=tg_id, full_name=full_name)
            session.add(user)
        await session.commit()

    await message.reply(f"Привіт, {full_name}! Вітаємо в Osnabrück Farm Connect. Реєстрація успішна.")

def register_start_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command("start"))