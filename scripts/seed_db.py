import asyncio
import os
import sys

# Додаємо шлях до кореня, щоб Python бачив папку core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import async_session
from core.models import Product, Category

async def seed():
    async with async_session() as session:
        # Create categories first
        categories_data = [
            {"name": "Schwein", "slug": "schwein", "description": "Pork products from Homeyer"},
            {"name": "Rind", "slug": "rind", "description": "Beef products from Homeyer"},
            {"name": "Wurst", "slug": "wurst", "description": "Sausages from Homeyer"},
            {"name": "Mix", "slug": "mix", "description": "Mixed meat products"}
        ]

        categories = {}
        for cat_data in categories_data:
            cat = Category(
                name=cat_data["name"],
                slug=cat_data["slug"],
                description=cat_data["description"]
            )
            session.add(cat)
            categories[cat_data["name"]] = cat

        # Дані з твого фото (23 позиції)
        products_data = [
            # SCHWEIN
            {"name": "Nacken ohne Knochen", "price": 5.49, "unit": "кг", "cat": "Schwein"},
            {"name": "Hackfleisch vom Schwein", "price": 4.50, "unit": "кг", "cat": "Schwein"},
            {"name": "Schnitzel / Braten", "price": 5.90, "unit": "кг", "cat": "Schwein"},
            {"name": "Lummersteaks", "price": 6.90, "unit": "кг", "cat": "Schwein"},
            {"name": "Filet (Schwein)", "price": 8.99, "unit": "кг", "cat": "Schwein"},
            {"name": "Dicke Rippe", "price": 4.90, "unit": "кг", "cat": "Schwein"},
            {"name": "Spareribs", "price": 5.50, "unit": "кг", "cat": "Schwein"},
            {"name": "Gehacktes halb & halb", "price": 5.80, "unit": "кг", "cat": "Mix"},
            {"name": "Bauchfleisch", "price": 5.90, "unit": "кг", "cat": "Schwein"},
            {"name": "Schinkenbraten", "price": 5.90, "unit": "кг", "cat": "Schwein"},
            {"name": "Kotelett", "price": 5.90, "unit": "кг", "cat": "Schwein"},

            # RIND
            {"name": "Rindfleisch ohne Knochen", "price": 9.50, "unit": "кг", "cat": "Rind"},
            {"name": "Rinderhackfleisch", "price": 7.20, "unit": "кг", "cat": "Rind"},
            {"name": "Rouladen / Braten", "price": 13.50, "unit": "кг", "cat": "Rind"},
            {"name": "Suppenfleisch", "price": 8.50, "unit": "кг", "cat": "Rind"},
            {"name": "Beinscheibe", "price": 7.90, "unit": "кг", "cat": "Rind"},
            {"name": "Entrecote / Rumpsteak", "price": 19.50, "unit": "кг", "cat": "Rind"},
            {"name": "Filet (Rind)", "price": 29.90, "unit": "кг", "cat": "Rind"},

            # WURST
            {"name": "Bratwurst", "price": 8.00, "unit": "кг", "cat": "Wurst"},
            {"name": "Fleischwurst", "price": 8.50, "unit": "кг", "cat": "Wurst"},
            {"name": "Mettwurst", "price": 9.50, "unit": "кг", "cat": "Wurst"},
            {"name": "Leberwurst", "price": 8.00, "unit": "кг", "cat": "Wurst"},
            {"name": "Grützwurst", "price": 7.50, "unit": "кг", "cat": "Wurst"}
        ]

        for p_data in products_data:
            p = Product(
                name=p_data["name"],
                price=p_data["price"],
                unit=p_data["unit"],
                is_available=True,
                description=f"Fresh from Homeyer GmbH",
                category=categories[p_data["cat"]]
            )
            session.add(p)

        try:
            await session.commit()
            print(f"✅ Готово! Додано {len(categories_data)} категорій та {len(products_data)} продуктів до бази.")
        except Exception as e:
            await session.rollback()
            print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    asyncio.run(seed())