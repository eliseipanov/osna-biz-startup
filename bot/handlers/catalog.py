from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from core.database import async_session
from core.models import Product

router = Router()

@router.message(F.text == "🥩 Каталог")
async def catalog_handler(message: Message):
    async with async_session() as session:
        query = select(Product).where(Product.is_available == True)
        result = await session.scalars(query)
        products = result.all()
        if products:
            text = "<b>Каталог продуктів:</b>\n"
            for p in products:
                text += f"{p.name} - {p.price} €/{p.unit}\n"
        else:
            text = "Каталог порожній."
        await message.answer(text, parse_mode="HTML")