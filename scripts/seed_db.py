import asyncio
import os
import sys

# Додаємо шлях до кореня, щоб Python бачив папку core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import async_session
from core.models import Product, Category, Translation
from sqlalchemy import text

async def seed():
    async with async_session() as session:
        # Hard reset: truncate tables
        await session.execute(text("TRUNCATE categories, products, translations RESTART IDENTITY CASCADE;"))
        await session.commit()

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

        # Add translations
        translations_data = [
            {"key": "welcome_message", "value_uk": "Вітаємо в Osnabrück Farm Connect!", "value_de": "Willkommen bei Osnabrück Farm Connect!"},
            {"key": "catalog_button", "value_uk": "🥩 Каталог", "value_de": "🥩 Katalog"},
            {"key": "cart_button", "value_uk": "🛒 Кошик", "value_de": "🛒 Warenkorb"},
            {"key": "orders_button", "value_uk": "📋 Мої замовлення", "value_de": "📋 Meine Bestellungen"},
            {"key": "profile_button", "value_uk": "👤 Профіль", "value_de": "👤 Profil"},
        ]

        for trans_data in translations_data:
            trans = Translation(
                key=trans_data["key"],
                value_uk=trans_data["value_uk"],
                value_de=trans_data["value_de"]
            )
            session.add(trans)

        try:
            await session.commit()
            print(f"✅ Database reset complete! Added {len(categories_data)} categories, {len(products_data)} products, and {len(translations_data)} translations.")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(seed())