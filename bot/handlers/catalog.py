from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "🥩 Каталог")
async def catalog_handler(message: Message):
    await message.answer("Завантажую актуальний прайс від фермерства Homeyer... 🥩")