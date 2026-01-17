from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from core.database import async_session
from core.models import Product, AvailabilityStatus

router = Router()

@router.message(F.text == "🥩 Каталог")
async def catalog_handler(message: Message):
    try:
        async with async_session() as session:
            query = select(Product).where(Product.availability_status == AvailabilityStatus.IN_STOCK)
            result = await session.scalars(query)
            products = result.all()
            if products:
                text = "<b>Каталог продуктів:</b>\n"
                for p in products:
                    text += f"{p.name} - {p.price} €/{p.unit}\n"
            else:
                text = "Каталог порожній."
    except Exception as e:
        text = "Сталася помилка при завантаженні каталогу. Спробуйте ще раз."
    await message.answer(text, parse_mode="HTML")