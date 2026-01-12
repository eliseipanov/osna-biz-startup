import asyncio
from core.database import async_session
from core.models import Product

async def seed():
    async with async_session() as session:
        products = [
            Product(name="Rumpsteak (Яловичина)", price=32.0, unit="кг", is_available=True, description=""),
            Product(name="Entrecôte (Яловичина)", price=35.0, unit="кг", is_available=True, description=""),
            Product(name="Bratwurst (Ковбаски)", price=12.5, unit="кг", is_available=True, description=""),
            Product(name="Schnitzel (Свинина)", price=14.0, unit="кг", is_available=True, description=""),
        ]
        for p in products:
            session.add(p)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())