from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from sqlalchemy import select

from core.database import async_session
from core.models import User
from bot.keyboards.main_menu import get_main_menu_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    tg_id = message.from_user.id
    full_name = message.from_user.full_name

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user is None:
            user = User(tg_id=tg_id, full_name=full_name)
            session.add(user)
            await session.commit()

    await message.answer("Вітаємо в Osnabrück Farm Connect! Оберіть розділ нижче 👇", reply_markup=get_main_menu_keyboard())