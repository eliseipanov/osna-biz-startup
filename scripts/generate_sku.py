import asyncio
import sys
import os

# Додаємо кореневу директорію проекту до шляхів пошуку модулів
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import AsyncSessionLocal, engine
from core.models import Product, Category, Farm

def slugify(text: str) -> str:
    if not text:
        return "GEN"
    # Робимо короткий префікс з великих літер (перші 3-4 літери)
    return text.strip().upper()[:4].replace(" ", "")

async def fill_missing_skus():
    # Використовуємо AsyncSessionLocal, який зазвичай є у нашому core/database.py
    async with AsyncSessionLocal() as session:
        # Отримуємо всі продукти, у яких SKU порожній або None
        result = await session.execute(
            select(Product).where((Product.sku == None) | (Product.sku == ""))
        )
        products = result.scalars().all()

        if not products:
            print("✅ Всі продукти вже мають SKU. Нічого оновлювати.")
            return

        print(f"🔄 Знайдено {len(products)} продуктів без SKU. Починаємо генерацію...")

        for product in products:
            # Завантажуємо категорію та ферму для створення гарного коду
            res_cat = await session.execute(select(Category).where(Category.id == product.category_id))
            category = res_cat.scalar_one_or_none()
            
            res_farm = await session.execute(select(Farm).where(Farm.id == product.farm_id))
            farm = res_farm.scalar_one_or_none()

            # Префікси на основі німецьких назв (як у ROADMAP)
            cat_prefix = slugify(category.name_de if category else "MEAT")
            farm_prefix = slugify(farm.name if farm else "OSNA")
            
            # Формуємо SKU: КАТ-ФЕРМА-ID (наприклад: PORK-OSNA-001)
            new_sku = f"{cat_prefix}-{farm_prefix}-{product.id:03d}"
            
            product.sku = new_sku
            print(f"📦 Створено SKU для '{product.name}': {new_sku}")

        await session.commit()
        print("🚀 Всі зміни збережено в базі даних!")

if __name__ == "__main__":
    try:
        asyncio.run(fill_missing_skus())
    except Exception as e:
        print(f"❌ Помилка під час виконання: {e}")
        print("\n💡 Якщо помилка 'ImportError', перевір назву сесії в core/database.py.")